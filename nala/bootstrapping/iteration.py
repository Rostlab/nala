import glob
import json
import os
import re
import time
import csv

from collections import defaultdict
from itertools import product, chain, count
from nala.bootstrapping.utils import UniprotDocumentSelector, PMIDDocumentSelector
from nala.structures.selection_pipelines import DocumentSelectorPipeline
from nala.bootstrapping.document_filters import HighRecallRegexDocumentFilter, ManualDocumentFilter, ManualStatsDocumentFilter
from nala.bootstrapping.pmid_filters import AlreadyConsideredPMIDFilter
from nala.learning.postprocessing import PostProcessing
from nalaf import print_verbose, print_debug
from nalaf.learning.crfsuite import PyCRFSuite
from nala.utils import nala_repo_path
from nalaf.utils.annotation_readers import AnnJsonAnnotationReader, AnnJsonMergerAnnotationReader
from nalaf.utils.readers import HTMLReader
from nalaf.preprocessing.labelers import BIEOLabeler
from nalaf.learning.evaluators import MentionLevelEvaluator
from nalaf.utils.writers import TagTogFormat
from nala.preprocessing.definers import ExclusiveNLDefiner
from nala.utils import MUT_CLASS_ID, THRESHOLD_VALUE
from nalaf.structures.data import Entity
from nalaf.domain.bio.gnormplus import GNormPlusGeneTagger
from nalaf.structures.data import Dataset

from nala.utils import get_prepare_pipeline_for_best_model


class IterationRound:
    """
    Class to represent a single iteration round

    For the future, likely this class should be renamed to Iteration and Iteration to sth like IterationPipeline
    """

    bootstrapping_folder = nala_repo_path(["resources", "bootstrapping"])

    def __init__(self, name, number=None, path=None):
        self.name = str(name)
        match = re.search('([0-9]+).*$', self.name)
        self.number = int(number) if number else int(match.group(1))
        self.path = path if path else os.path.join(IterationRound.bootstrapping_folder, "iteration_" + self.name)

    def is_seed(self):
        return self.number == 0

    def is_test(self):
        return "test" in self.name

    def is_random(self):
        return "random" in self.name

    def is_training(self):
        return not (self.is_test() or self.is_random())

    def is_IAA(self):
        return "IAA" in self.name

    def is_reviewed(self):
        return (os.path.isdir(os.path.join(self.path, 'candidates')) and
            os.path.isdir(os.path.join(self.path, 'reviewed')))

    def __str__(self):
        return "Iteration: {} : {}".format(self.name, self.path)

    def __repr__(self):
        return self.__str__()

    def read(self, read_annotations=True):
        print_debug(self)
        dataset = None

        if self.is_seed():
            base_folder = os.path.join(self.path, 'base')
            html_folder = os.path.join(base_folder, 'html')
            annjson_folder = os.path.join(base_folder, 'annjson')

            dataset = HTMLReader(html_folder).read()
            if read_annotations:
                AnnJsonMergerAnnotationReader(
                    os.path.join(annjson_folder, 'members'),
                    read_only_class_id=MUT_CLASS_ID,
                    strategy='intersection',
                    entity_strategy='priority',
                    priority=['Ectelion', 'abojchevski', 'sanjeevkrn', 'Shpendi'],
                    delete_incomplete_docs=True).annotate(dataset)

        elif self.is_IAA():
            base_folder = self.path
            html_folder = os.path.join(base_folder, 'candidates', 'html')
            annjson_folder = os.path.join(base_folder, 'reviewed')

            dataset = HTMLReader(html_folder).read()
            if read_annotations:
                AnnJsonMergerAnnotationReader(
                    annjson_folder,
                    read_only_class_id=MUT_CLASS_ID,
                    strategy='intersection',
                    entity_strategy='priority',
                    priority=['cuhlig', 'abojchevski', 'jmcejuela'],
                    delete_incomplete_docs=False).annotate(dataset)

        else:
            base_folder = self.path
            html_folder = os.path.join(base_folder, 'candidates', 'html')
            annjson_folder = os.path.join(base_folder, 'reviewed')

            dataset = HTMLReader(html_folder).read()
            if read_annotations:
                AnnJsonAnnotationReader(annjson_folder, read_only_class_id=MUT_CLASS_ID, delete_incomplete_docs=False, read_relations=self.is_random()).annotate(dataset)

        print_debug("\t", dataset.__repr__())
        return dataset

    @staticmethod
    def all(including_seed=True):
        ret = []
        for fn in glob.glob(IterationRound.bootstrapping_folder + "/iteration_*/"):
            match = re.search('iteration_(([0-9]+).*)/$', fn)
            if match:
                ret.append(IterationRound(
                    name=match.group(1),
                    number=int(match.group(2)),
                    path=fn))

        ret.sort(key=lambda x: x.number)

        if not including_seed:
            ret = ret[1:]

        return ret

    @staticmethod
    def find_last_iteration_number():
        last = IterationRound.all()[-1]

        # check for candidates and reviewed
        if last.number == 0:
            return 1
        elif last.is_reviewed:
            return last.number + 1
        else:
            return last.number


class Iteration:
    """
    This is the class to perform one iteration of bootstrapping. There are various options.

    :type candidates: nalaf.structures.data.Dataset
    """
    # TODO finish docset of Iteration Class
    def __init__(self, folder=None, iteration_nr=None, threshold_val=THRESHOLD_VALUE, pipeline=None, stats=False):
        """
        Init function of iteration. Has to be called with proper folder and crfsuite path if not default.
        :param folder: Bootstrapping folder (has to be created before including base folder with html + annjson folder and corpus)
        :param iteration_nr: In which iteration the bootstrapping process is currently. Effects self.current_folder
        :param threshold_val: The threshold value to select annotations to pre-added or selected to semi-supervise.
        """
        super().__init__()
        # TODO major sophisticated automatic execution (check what is missing e.g. bin_model)
        if folder is not None:
            self.bootstrapping_folder = os.path.abspath(folder)
        else:
            self.bootstrapping_folder = IterationRound.bootstrapping_folder

        if not os.path.isdir(self.bootstrapping_folder):
            raise FileNotFoundError('''
            The bootstrapping folder does not exist.
            And needs to be created including with the annotated starting corpus.
            ''', self.bootstrapping_folder)

        # threshold class-wide variable to save in stats.csv file
        self.threshold_val = threshold_val

        # empty init variables
        self.train = None  # first
        self.candidates = None  # non predicted docselected
        self.predicted = None  # predicted docselected
        self.crf = PyCRFSuite()

        # preparedataset pipeline init
        if not stats:
            if pipeline is None or not isinstance(pipeline, PrepareDatasetPipeline):
                self.pipeline = get_prepare_pipeline_for_best_model()
                """ :type PrepareDatasetPipeline: """
            else:
                self.pipeline = pipeline
                """ :type PrepareDatasetPipeline: """
        else:
            self.pipeline = None

        # labeler init
        self.labeler = BIEOLabeler()

        # discussion on config file in bootstrapping root or iteration_n check for n
        # note currently using parameter .. i think that s the most suitable

        print_verbose('Check for Iteration Number....')

        # TODO make state checks (e.g. has bin model, reviewed files, candidates, results)

        if iteration_nr is None:
            self.number = IterationRound.find_last_iteration_number()
        else:
            self.number = iteration_nr

        # current folders
        self.current_folder = os.path.join(self.bootstrapping_folder, "iteration_{}".format(self.number))
        self.candidates_folder = os.path.join(self.current_folder, 'candidates')
        self.reviewed_folder = os.path.join(self.current_folder, 'reviewed')

        if not os.path.exists(os.path.join(self.current_folder)):
            os.mkdir(os.path.join(self.current_folder))

        # binary model
        self.bin_model = os.path.join(self.current_folder, 'bin_model')

        # stats file
        self.stats_file = os.path.join(self.bootstrapping_folder, 'stats.csv')
        self.results_file = os.path.join(self.current_folder, 'batch_results.txt')
        self.debug_file = os.path.join(self.current_folder, 'debug.txt')

        print_verbose('Initialisation of Iteration instance finished.')

        if not os.path.exists(self.stats_file):
            with open(self.stats_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['iteration_number', 'subclass', 'threshold',
                                 'tp', 'fp', 'fn', 'fp_overlap', 'fn_overlap', 'precision', 'recall', 'f1-score'])


    def before_annotation(self, nr_new_docs=10):
        self.learning()
        self.docselection(nr=nr_new_docs)
        self.tagging(threshold_val=self.threshold_val)

    def after_annotation(self):
        self.clean_reviewed_files()
        self.manual_review_import()
        self.evaluation()

    def read_learning_data(self):
        """
        Loads and parses the annotations from base + following iterations into self.train
        """
        print_verbose("\n\n####ParseData####\n")

        self.train = Iteration.read_IDP4Plus_training()

        print_verbose(len(self.train.documents), "documents are used in the training dataset.")

    @staticmethod
    def read_IDP4():
        return IterationRound(0).read()

    @staticmethod
    def read_nala():
        dataset = Iteration.read_nala_training()
        dataset.extend_dataset(Iteration.read_nala_test())
        return dataset

    @staticmethod
    def read_nala_training(until_iteration=None):
        """
        optional until_iteration: only read from 1 to this iteration, otherwise read all iterations
        """
        dataset = Dataset()
        itrs = IterationRound.all(including_seed=False)
        if until_iteration:
            itrs = itrs[:until_iteration]

        for itr in itrs:
            if itr.is_training():
                try:
                    dataset.extend_dataset(itr.read())
                except FileNotFoundError as e:
                    print_debug(e)
                    continue

        return dataset


    @staticmethod
    def read_nala_test(number_iterations=-1):
        dataset = Dataset()

        number_iterations = -1 if number_iterations is None else number_iterations

        for itr in IterationRound.all(including_seed=False):
            if (number_iterations == 0):
                break

            else:
                if itr.is_test():
                    try:
                        dataset.extend_dataset(itr.read())
                        number_iterations -= 1

                    except FileNotFoundError as e:
                        print_debug(e)
                        continue

        return dataset

    @staticmethod
    def read_nala_random():
        dataset = Dataset()
        for itr in IterationRound.all(including_seed=False):
            if itr.is_random():
                try:
                    dataset.extend_dataset(itr.read())
                except FileNotFoundError as e:
                    print_debug(e)
                    continue

        return dataset

    @staticmethod
    def read_IDP4Plus():
        dataset = Iteration.read_IDP4()
        dataset.extend_dataset(Iteration.read_nala())
        return dataset

    @staticmethod
    def read_IDP4Plus_training(until_iteration=None):
        dataset = Iteration.read_IDP4()
        dataset.extend_dataset(Iteration.read_nala_training(until_iteration))
        return dataset

    @staticmethod
    def read_IDP4Plus_test():
        return Iteration.read_nala_test()


    def preprocessing(self):
        """
        Pre-processing including pruning, generating features, generating labels.
        """
        print_verbose("\n\n####PreProcess####\n")
        # prune parts without annotations
        self.train.prune_empty_parts()

        # prepare features
        print_verbose("##PreparePipeline##")
        self.pipeline.execute(self.train)
        self.pipeline.serialize(self.train, to_file=self.debug_file)

        # labeling
        print_verbose("##Labeling##")
        self.labeler.label(self.train)

        print_verbose(len(self.train.documents), "documents are prepared for training dataset.")

    def crf_learning(self):
        """
        Learning: base + iterations 1..n-1
        just the crfsuitepart and copying the model to the iteration folder
        """
        print_verbose("\n\n####Learning####\n")

        # crfsuite part
        # self.crf.create_input_file(self.train, 'train')
        # self.crf.learn()
        self.crf.train(self.train, self.bin_model)


    def learning(self):
        """
        import files
        preprocess data
        run crfsuite on data
        """
        print_verbose("####learning####")
        self.read_learning_data()

        if not os.path.exists(self.bin_model):
            self.preprocessing()
            self.crf_learning()
        else:
            print_verbose("Already existing binary model is used.")
        print_verbose('Model at "{}".'.format(self.bin_model))

    def docselection_pmids(self, nr, pmids):

        dataset = Dataset()
        doc_filter = ManualStatsDocumentFilter(['nl', 'st'])

        with DocumentSelectorPipeline(
                document_selector=PMIDDocumentSelector(pmids),
                pmid_filters=[AlreadyConsideredPMIDFilter(self.bootstrapping_folder, self.number)],
                document_filters=[doc_filter]) as dsp:

            for pmid, document in dsp.execute():
                dataset.documents[pmid] = document

                print_verbose('Documents found: {}'.format(doc_filter.counter))

                # if we have generated enough documents stop
                if doc_filter.counter['nl'] == nr:
                    break

        self.candidates = dataset
        len_cand = len(self.candidates)
        if len_cand < nr:
            exit('Not {} documents as expected. Only {}'.format(nr, len_cand))

        print("\n\n\n", doc_filter.answers, "\n\n", doc_filter.counter, "\n\n\n")

        # export to anndoc format
        ttf_candidates = TagTogFormat(self.candidates, use_predicted=False, to_save_to=self.candidates_folder, use_original_partids=False)
        ttf_candidates.export_html()
        ttf_candidates.export_ann_json(THRESHOLD_VALUE)

        return doc_filter

    def docselection(self, nr=2, just_caching=False):
        """
        Does the same as generate_documents(n) but the bootstrapping folder is specified in here.
        :param nr: amount of new documents wanted
        """
        print_verbose("\n\n\n======DocSelection======\n\n\n")


        c = count(1)

        dataset = Dataset()

        if just_caching:
            _counter = 0
            _total = 0
            with DocumentSelectorPipeline(
                    document_selector=UniprotDocumentSelector(),
                    pmid_filters=[AlreadyConsideredPMIDFilter(self.bootstrapping_folder, self.number)]
                    ) as dsp:
                _starttime = time.perf_counter()
                _already_downloaded = 0
                for pmid, document in dsp.execute():

                    dataset.documents[pmid] = document

                    _counter += 1
                    _tmptime = time.perf_counter()
                    _one_it = _tmptime - _starttime
                    _starttime = _tmptime

                    if _one_it < 0.25:  # check if not already downloaded (for eta calculation)
                        _already_downloaded += 1
                        _counter -= 1
                        _total -= _one_it

                    _total += _one_it
                    # print_verbose('total', _total)
                    if _counter > 0:
                        _eta_one = _total / _counter
                        _counter_left = nr - _counter - _already_downloaded
                        _eta_left = _eta_one * _counter_left
                        print_verbose(
                            'NrOfDocs: {} | ETA Left for {}: {:.3f} | ETA One for One: {:.3f}'.format(_counter, _counter_left,
                                                                                          _eta_left, _eta_one))

                    # if we have generated enough documents stop
                    if next(c) == nr:
                        break
        else:
            with DocumentSelectorPipeline(
                    document_selector=UniprotDocumentSelector(),
                    pmid_filters=[AlreadyConsideredPMIDFilter(self.bootstrapping_folder, self.number)],
                    document_filters=[HighRecallRegexDocumentFilter(binary_model=self.bin_model,
                                                                    expected_max_results=nr, use_nala=True),
                                      ManualDocumentFilter()]) as dsp:
                for pmid, document in dsp.execute():
                    dataset.documents[pmid] = document
                    lendata = len(dataset.documents)
                    print_verbose('Already {} documents found. {} more to go.'.format(lendata, nr - lendata))

                    # if we have generated enough documents stop
                    if next(c) == nr:
                        break

        self.candidates = dataset
        len_cand = len(self.candidates)
        if len_cand < nr:
            exit('Not {} documents as expected. only {}'.format(nr, len_cand))

    # TODO rename to annotate
    def tagging(self, threshold_val=THRESHOLD_VALUE):
        print_verbose("\n\n\n======Tagging======\n\n\n")

        self.pipeline.execute(self.candidates)
        self.crf.tag(self.candidates, self.bin_model, MUT_CLASS_ID)
        PostProcessing().process(self.candidates)
        GNormPlusGeneTagger().tag(self.candidates)

        self.candidates.validate_entity_offsets()

        # export to anndoc format
        ttf_candidates = TagTogFormat(self.candidates, use_predicted=True, to_save_to=self.candidates_folder, use_original_partids=False)
        ttf_candidates.export_html()
        ttf_candidates.export_ann_json(threshold_val)

    def manual_review_import(self):
        """
        Parse from iteration_n/reviewed folder in anndoc format.
        :return:
        """
        self.reviewed = HTMLReader(os.path.join(self.candidates_folder, 'html')).read()

        AnnJsonAnnotationReader(os.path.join(self.candidates_folder, 'annjson'),
                                read_only_class_id=MUT_CLASS_ID, is_predicted=True,
                                delete_incomplete_docs=False).annotate(self.reviewed)

        AnnJsonAnnotationReader(os.path.join(self.reviewed_folder), read_only_class_id=MUT_CLASS_ID, delete_incomplete_docs=False).annotate(self.reviewed)
        # automatic evaluation

    def evaluation(self):
        """
        When Candidates and Reviewed are existing do automatic evaluation and calculate performances
        :return:
        """
        ExclusiveNLDefiner().define(self.reviewed)

        # debug results / annotations
        results = []
        for part in self.reviewed.parts():
            not_found_ann = part.annotations[:]
            not_found_pred = part.predicted_annotations[:]
            for ann, pred in product(part.annotations, part.predicted_annotations):
                Entity.equality_operator = 'exact_or_overlapping'
                if ann == pred:
                    results.append((ann, pred))

                    # delete found elements
                    if ann in not_found_ann:
                        index = not_found_ann.index(ann)
                        del not_found_ann[index]

                    if pred in not_found_pred:
                        index = not_found_pred.index(pred)
                        del not_found_pred[index]
            results += [(ann, Entity(class_id='e_2', offset=-1, text='')) for ann in not_found_ann]
            results += [(Entity(class_id='e_2', offset=-1, text=''), pred) for pred in not_found_pred]

        annotated_format = "{:<" + str(max(chain(len(x.text) for x in self.reviewed.annotations()))) + "}"
        predicted_format = "{:<" + str(max(chain(len(x.text) for x in self.reviewed.predicted_annotations()))) + "}"
        row_format = annotated_format + '\t|\t' + predicted_format + "\n"

        with open(self.results_file, 'w', encoding='utf-8') as f:
            f.write(row_format.format('=====Annotated=====', '=====Predicted====='))
            for tuple in ((x[0].text, x[1].text) for x in results):
                f.write(row_format.format(*tuple))
            f.write('-'*80)
            f.write('\n\n=====Detailed Results=====\n')
            f.write(
                'Exact:            TP={}\tFP={}\tFN={}\tFP_OVERLAP={}\tFN_OVERLAP={}\tPREC={:.3%}\tRECALL={:.3%}\tF-MEAS={:.3%}\n'.format(
                    *MentionLevelEvaluator().evaluate(self.reviewed)))
            f.write(
                'Overlapping:      TP={}\tFP={}\tFN={}\tFP_OVERLAP={}\tFN_OVERLAP={}\tPREC={:.3%}\tRECALL={:.3%}\tF-MEAS={:.3%}\n'.format(
                    *MentionLevelEvaluator(strictness='overlapping').evaluate(self.reviewed)))
            f.write(
                'Half-Overlapping: TP={}\tFP={}\tFN={}\tFP_OVERLAP={}\tFN_OVERLAP={}\tPREC={:.3%}\tRECALL={:.3%}\tF-MEAS={:.3%}\n'.format(
                    *MentionLevelEvaluator(strictness='half_overlapping').evaluate(self.reviewed)))
            subclass_string = json.dumps(MentionLevelEvaluator(subclass_analysis=True).evaluate(self.reviewed)[0],
                                         indent=4, sort_keys=True)
            f.write('Raw-Data:\n{}'.format(subclass_string))

        # optional containing sentence
        # optional containing document-id
        # optional group according to subclass (different sizes)

    def cross_validation(self, split):
        """
        does k fold cross validation with split being k
        :param split: int
        """
        base_folder = os.path.join(os.path.join(self.bootstrapping_folder, 'iteration_0'), 'base')
        data = HTMLReader(os.path.join(base_folder, 'html')).read()
        AnnJsonMergerAnnotationReader(os.path.join(os.path.join(base_folder, 'annjson'), 'members'),
                                      read_only_class_id=MUT_CLASS_ID,
                                      strategy='intersection', entity_strategy='priority',
                                      priority = ['Ectelion', 'abojchevski', 'sanjeevkrn', 'Shpendi'],
                                      delete_incomplete_docs=True).annotate(data)
        print_verbose(len(data), 'documents in base')

        for fold in range(1, self.number):
            iteration_base = os.path.join(self.bootstrapping_folder, "iteration_{}".format(fold))

            tmp_data = HTMLReader(os.path.join(os.path.join(iteration_base, 'candidates'), 'html')).read()
            AnnJsonAnnotationReader(os.path.join(iteration_base, 'reviewed'), read_only_class_id=MUT_CLASS_ID, delete_incomplete_docs=False).annotate(tmp_data)
            data.extend_dataset(tmp_data)
        print_verbose(len(data), 'documents in total')

        last_iteration = os.path.join(self.bootstrapping_folder, "iteration_{}".format(self.number-1))
        cv_file = os.path.join(last_iteration, 'cross_validation.csv')
        with open(cv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['fold', 'strictness', 'sublcass',
                             'tp', 'fp', 'fn', 'fp_overlap', 'fn_overlap',
                             'precision', 'recall', 'f1-score'])

        folds_results_exact = []
        folds_results_overlapping = []
        subclass_averages_exact = defaultdict(list)
        subclass_averages_overlapping = defaultdict(list)

        for fold, (train, test) in enumerate(data.cv_split(5)):
            print_verbose('starting with fold:', fold)

            train.prune_empty_parts()
            self.pipeline.execute(train)
            BIEOLabeler().label(train)
            self.crf.train(train, 'cross_validation_model')

            self.pipeline.execute(test)
            BIEOLabeler().label(test)
            self.crf.tag(test, 'cross_validation_model')

            ExclusiveNLDefiner().define(test)
            PostProcessing().process(test)

            with open(cv_file, 'a', newline='') as file:
                writer = csv.writer(file)

                subclass_measures, results = MentionLevelEvaluator(strictness='exact', subclass_analysis=True).evaluate(test)
                for subclass, measures in subclass_measures.items():
                    writer.writerow(list(chain([fold, 'exact', int(subclass)], measures)))
                    subclass_averages_exact[subclass].append(measures)
                writer.writerow(list(chain([fold, 'exact', 'total'], results)))
                folds_results_exact.append(results)

                subclass_measures, results = MentionLevelEvaluator(strictness='overlapping', subclass_analysis=True).evaluate(test)
                for subclass, measures in subclass_measures.items():
                    writer.writerow(list(chain([fold, 'overlapping', int(subclass)], measures)))
                    subclass_averages_overlapping[subclass].append(measures)
                writer.writerow(list(chain([fold, 'overlapping', 'total'], results)))
                folds_results_overlapping.append(results)

        # calculate and write average of folds
        with open(cv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            # ================== EXACT =================
            for subclass, averages in subclass_averages_exact.items():
                writer.writerow(list(chain(['average', 'exact', subclass],
                                           [sum(col)/len(col) for col in zip(*averages)])))
            # average out everything in the columns
            writer.writerow(list(chain(['average', 'exact', 'total'],
                                       [sum(col)/len(col) for col in zip(*folds_results_exact)])))

            # =============== OVERLAPPING ===============
            for subclass, averages in subclass_averages_overlapping.items():
                writer.writerow(list(chain(['average', 'overlapping', subclass],
                                           [sum(col)/len(col) for col in zip(*averages)])))
            # average out everything in the columns
            writer.writerow(list(chain(['average', 'overlapping', 'total'],
                                       [sum(col)/len(col) for col in zip(*folds_results_overlapping)])))

            # =============== sum of folds ===============
            # sum up the counts (tp, fp, etc.) and then calculate the measures
            for subclass, averages in subclass_averages_exact.items():
                writer.writerow(list(chain(['sum_of_folds', 'exact', subclass],
                                           MentionLevelEvaluator(strictness='exact').calc_measures(
                                                   *[sum(col) for col in zip(*averages)][:5]))))
            writer.writerow(list(chain(['sum_of_folds', 'exact', 'total'],
                                       MentionLevelEvaluator(strictness='exact').calc_measures(
                                               *[sum(col) for col in zip(*folds_results_exact)][:5]))))

            with open(self.stats_file, 'a',  newline='') as stats_write_file:
                stats_writer = csv.writer(stats_write_file)
                for subclass, averages in subclass_averages_exact.items():
                    stats = MentionLevelEvaluator(strictness='overlapping').calc_measures(
                            *[sum(col) for col in zip(*averages)][:5])
                    writer.writerow(list(chain(['sum_of_folds', 'overlapping', subclass], stats)))
                    stats_writer.writerow([self.number-1, subclass, self.threshold_val] + list(stats))

                stats = MentionLevelEvaluator(strictness='overlapping').calc_measures(
                        *[sum(col) for col in zip(*folds_results_exact)][:5])
                writer.writerow(list(chain(['sum_of_folds', 'overlapping', 'total'], stats)))
                stats_writer.writerow([self.number-1, 'total', self.threshold_val] + list(stats))

    def clean_reviewed_files(self):
        import re
        candidates = HTMLReader(os.path.join(self.candidates_folder, 'html')).read()
        for (dirpath, dirnames, filenames) in os.walk(self.reviewed_folder):
            for filename in filenames:
                docid = re.sub(r'.*-(\d+)\..*', r'\1', filename)
                if docid not in candidates.documents.keys():
                    os.remove(os.path.join(dirpath, filename))

import argparse
import os
import sys
import tempfile
from nala.preprocessing.definers import ExclusiveNLDefiner
from nala.utils.corpora import get_corpus, get_corpora
from nalaf.preprocessing.labelers import BIEOLabeler, BIOLabeler, IOLabeler, TmVarLabeler
from nala.utils import get_prepare_pipeline_for_best_model, get_prepare_pipeline_for_best_model_general
from nalaf.learning.crfsuite import PyCRFSuite
from nalaf.learning.evaluators import MentionLevelEvaluator
from nala.learning.taggers import NalaSingleModelTagger, NalaMultipleModelTagger
from nalaf.utils.writers import TagTogFormat
from nala.bootstrapping.document_filters import HighRecallRegexClassifier
from nalaf.utils.readers import StringReader
from nalaf.utils.writers import ConsoleWriter
from nalaf import print_debug
import time
from nala.utils import MUT_CLASS_ID, PRO_CLASS_ID


def train(argv):
    parser = argparse.ArgumentParser(description='Train model')

    parser.add_argument('--training_corpus',
                        help='Name of the corpus to train on. Ex: nala_training, IDP4+_training, nala_training_5')
    parser.add_argument('--test_corpus',
                        help='Name of the corpus to test on')
    parser.add_argument('--string',
                        help='String to tag')

    parser.add_argument('--validation', required=False, default="stratified",
                        choices=["cross-validation", "stratified", "none"],
                        help='Type of validation to use when training')

    parser.add_argument('--cv_n', required=False,
                        help='if given, cross validation (instead of stratification) is used for validating the training. \
                        In this case you must also set `cv_fold` and only that fold number will be run')
    parser.add_argument('--cv_fold', required=False,
                        help='fold number if cross validation is activated (it starts at 0; i.e. for cv_n=5, you have folds: [0,1,2,3,4] )')

    parser.add_argument('--output_folder', required=False,
                        help='Folder where the training model is written to. Otherwise a tmp folder is used')
    parser.add_argument('--model_name_suffix', default='', required=False,
                        help='Optional suffix to add to the generated model name in training mode'),
    parser.add_argument('--write_anndoc', required=False, default=False, action='store_true',
                        help='Write anndoc of predicted test_corpus (validation corpus in fact)'),
    parser.add_argument('--model_path_1', required=False,
                        help='Path of the first model binary file if evaluation is performed')
    parser.add_argument('--model_path_2', required=False,
                        help='Path of the second model binary file if evaluation is performed with two models')

    parser.add_argument('--labeler', required=False, default="BIEO", choices=["BIEO", "BIO", "IO", "11labels"],
                        help='Labeler to use for training')

    parser.add_argument('--mutations_specific', default='True',
                        help='Apply feature pipelines specific to mutations or otherwise (false) use general one')

    parser.add_argument('--only_class_id', required=False, default=MUT_CLASS_ID,
                        help="By default, only the mutation entities are read from corpora (assumed to have class_id == '" + MUT_CLASS_ID + "'). Set this class_id to filter rest out")
    parser.add_argument('--delete_subclasses', required=False, default="",
                        help='Comma-separated subclasses to delete. Example: "2,3"')

    parser.add_argument('--pruner', required=False, default="parts", choices=["parts", "sentences"])
    parser.add_argument('--ps_ST', required=False, default=False, action='store_true')
    parser.add_argument('--ps_NL', required=False, default=False, action='store_true')
    parser.add_argument('--ps_random', required=False, default=0.0, type=float)

    parser.add_argument('--elastic_net', action='store_true',
                        help='Use elastic net regularization')

    parser.add_argument('--word_embeddings', '--we', default='True', help='Use word embeddings features')
    parser.add_argument('--we_additive', type=float, default=0)
    parser.add_argument('--we_multiplicative', type=float, default=1)
    parser.add_argument('--we_model_location', type=str, default=None)

    parser.add_argument('--use_feat_windows', default='True')

    parser.add_argument('--nl', action='store_true', help='Use NLMentionFeatureGenerator')
    parser.add_argument('--nl_threshold', type=int, default=0)
    parser.add_argument('--nl_window', action='store_true', help='use window feature for NLFeatureGenerator')

    parser.add_argument('--execute_pp', default='True',
                        help='Execute post processing specific to mutations (default) or not')
    parser.add_argument('--keep_silent', default='True',
                        help='Keep silent mutations (default) or not, i.e., delete mentions like `Cys23-Cys`')
    parser.add_argument('--keep_genetic_markers', default='True',
                        help='Keep genetic markers of the form D17S250, true (default) or false')
    parser.add_argument('--keep_unnumbered', default='True',
                        help='Keep unnumbered mentions (default) or not, i.e., delete mentions like `C -> T`')
    parser.add_argument('--keep_rs_ids', default='True',
                        help='Keep unnumbered mentions (default) or not, i.e., delete mentions like `rs1801280` or `ss221`')

    FALSE = ['false', 'f', '0', 'no', 'none']

    def arg_bool(arg_value):
        return False if arg_value.lower() in FALSE else True

    args = parser.parse_args(argv)

    start_time = time.time()

    # ------------------------------------------------------------------------------

    delete_subclasses = []
    for c in args.delete_subclasses.split(","):
        c.strip()
        if c:
            delete_subclasses.append(int(c))

    args.delete_subclasses = delete_subclasses

    if not args.output_folder:
        args.output_folder = tempfile.mkdtemp()

    str_delete_subclasses = "None" if not args.delete_subclasses else str(args.delete_subclasses).strip('[]').replace(' ', '')

    if args.labeler == "BIEO":
        labeler = BIEOLabeler()
    elif args.labeler == "BIO":
        labeler = BIOLabeler()
    elif args.labeler == "IO":
        labeler = IOLabeler()
    elif args.labeler == "11labels":
        labeler = TmVarLabeler()

    args.word_embeddings = arg_bool(args.word_embeddings)

    if args.word_embeddings:
        args.we_params = {
            'additive': args.we_additive,
            'multiplicative': args.we_multiplicative,
            'location': args.we_model_location
        }
    else:
        args.we_params = {}  # means: do not use we

    if args.nl:
        args.nl_features = {
            'threshold': args.nl_threshold,  # threshold for neighbour space in dictionaries
            'window': args.nl_window,
        }
    else:
        args.nl_features = None

    if args.elastic_net:
        args.crf_train_params = {
            'c1': 1.0,  # coefficient for L1 penalty
            'c2': 1e-3,  # coefficient for L2 penalty
        }
    else:
        args.crf_train_params = None

    args.use_feat_windows = False if args.use_feat_windows.lower() in FALSE else True
    args.mutations_specific = False if args.mutations_specific.lower() in FALSE else True
    args.execute_pp = False if args.execute_pp.lower() in FALSE else True
    args.keep_silent = False if args.keep_silent.lower() in FALSE else True
    args.keep_genetic_markers = False if args.keep_genetic_markers.lower() in FALSE else True
    args.keep_unnumbered = False if args.keep_unnumbered.lower() in FALSE else True
    args.keep_rs_ids = False if args.keep_rs_ids.lower() in FALSE else True

    args.do_train = False if args.model_path_1 else True

    if args.cv_n is not None or args.cv_fold is not None:
        args.validation = "cross-validation"

    if args.validation == "cross-validation":
        assert (args.cv_n is not None and args.cv_fold is not None), "You must set both cv_n AND cv_n"

    # ------------------------------------------------------------------------------

    if args.training_corpus:
        # Get the name of training corpus even if this is given as a folder path, in which case the last folder name is used
        training_corpus_name = list(filter(None, args.training_corpus.split('/')))[-1]

        args.model_name = "{}_{}_del_{}".format(training_corpus_name, args.labeler, str_delete_subclasses)

        if args.validation == "cross-validation":
            args.model_name += "_cvfold_" + str(args.cv_fold)
        args.model_name_suffix = args.model_name_suffix.strip()
        if args.model_name_suffix:
            args.model_name += "_" + str(args.model_name_suffix)

    else:
        args.model_name = args.test_corpus

    # ------------------------------------------------------------------------------

    def stats(dataset, name):
        print('\n\t{} size: {}'.format(name, len(dataset)))
        # Caveat: the dataset must be (mutations) defined first
        print('\tsubclass distribution: {}'.format(repr(dataset)))
        # Caveat: the dataset must be passed through the pipeline first
        print('\tnum sentences: {}\n'.format(sum(1 for x in dataset.sentences())))

    definer = ExclusiveNLDefiner()

    if args.training_corpus:
        train_set = get_corpus(args.training_corpus, args.only_class_id)

        if args.test_corpus:
            test_set = get_corpus(args.test_corpus, args.only_class_id)
        elif args.string:
            test_set = StringReader(args.string).read()
        elif args.validation == "none":
            test_set = None
        elif args.validation == "cross-validation":
            train_set, test_set = train_set.fold_nr_split(int(args.cv_n), int(args.cv_fold))
        elif args.validation == "stratified":
            definer.define(train_set)
            train_set, test_set = train_set.stratified_split()

    elif args.test_corpus:
        train_set = None
        test_set = get_corpora(args.test_corpus, args.only_class_id)

    elif args.string:
        train_set = None
        test_set = StringReader(args.string).read()

    else:
        raise Exception("you must give at least a parameter of: training_corpus, test_corpus, or string")

    def verify_corpus(corpus):
        if corpus is not None:
            assert len(corpus) > 0, 'The corpus has no documents: {}'.format(args.training_corpus)
            assert next(corpus.annotations(), None) is not None, 'The corpus has no annotations'

    verify_corpus(train_set)

    # ------------------------------------------------------------------------------

    if args.mutations_specific:
        print("Pipeline specific to mutations")
        features_pipeline = get_prepare_pipeline_for_best_model(args.use_feat_windows, args.we_params, args.nl_features)
    else:
        print("Pipeline is general")
        features_pipeline = get_prepare_pipeline_for_best_model_general(args.use_feat_windows, args.we_params, args.nl_features)

    # ------------------------------------------------------------------------------

    def print_run_args():
        for key, value in sorted((vars(args)).items()):
            print("\t{} = {}".format(key, value))
        print()

    print("Running arguments: ")

    print_run_args()

    # ------------------------------------------------------------------------------

    def train(train_set):
        definer.define(train_set)
        train_set.delete_subclass_annotations(args.delete_subclasses)
        features_pipeline.execute(train_set)
        labeler.label(train_set)

        if args.pruner == "parts":
            train_set.prune_empty_parts()
        else:
            try:
                f = HighRecallRegexClassifier(ST=args.ps_ST, NL=args.ps_NL)
            except AssertionError:
                f = (lambda _: False)
            train_set.prune_filtered_sentences(filterin=f, percent_to_keep=args.ps_random)

        stats(train_set, "training")

        crf = PyCRFSuite()

        model_path = os.path.join(args.output_folder, args.model_name + ".bin")
        crf.train(train_set, model_path, args.crf_train_params)

        return model_path

    # ------------------------------------------------------------------------------

    if args.do_train:
        args.model_path_1 = train(train_set)

    # ------------------------------------------------------------------------------

    def test(tagger, test_set, print_eval=True, print_results=False):
        tagger.tag(test_set)
        definer.define(test_set)
        stats(test_set, "test")
        evaluation = MentionLevelEvaluator(subclass_analysis=True).evaluate(test_set)

        print_run_args()

        if print_eval:
            print(evaluation)
        if print_results:
            ConsoleWriter(ent1_class_id=PRO_CLASS_ID, ent2_class_id=MUT_CLASS_ID, color=True).write(test_set)

    # ------------------------------------------------------------------------------

    assert(args.model_path_1 is not None)

    if args.model_path_2:
        tagger = NalaMultipleModelTagger(
                                       st_model=args.model_path_1,
                                       all3_model=args.model_path_2,
                                       features_pipeline=features_pipeline,
                                       execute_pp=args.execute_pp,
                                       keep_silent=args.keep_silent,
                                       keep_genetic_markers=args.keep_genetic_markers,
                                       keep_unnumbered=args.keep_unnumbered,
                                       keep_rs_ids=args.keep_rs_ids)
    else:
        tagger = NalaSingleModelTagger(bin_model=args.model_path_1,
                                       features_pipeline=features_pipeline,
                                       execute_pp=args.execute_pp,
                                       keep_silent=args.keep_silent,
                                       keep_genetic_markers=args.keep_genetic_markers,
                                       keep_unnumbered=args.keep_unnumbered,
                                       keep_rs_ids=args.keep_rs_ids)

    # ------------------------------------------------------------------------------

    print("\n{}".format(args.model_name))

    if train_set:
        stats(train_set, "training")

    if test_set:
        test(tagger, test_set, print_eval=args.string is None, print_results=args.string is not None)

    if args.do_train:
        print("\nThe model is saved to: {}\n".format(args.model_path_1))

    if args.write_anndoc:
        outdir = os.path.join(args.output_folder, args.model_name)
        os.mkdir(outdir)
        print("\nThe predicted test data is saved to: {}\n".format(outdir))
        TagTogFormat(test_set, use_predicted=True, to_save_to=outdir).export(0)

    end_time = time.time()

    print_debug("Elapsed time: ", (end_time - start_time))

    return {
        "tagger": tagger,
        "trained_model_path": args.model_path_1,
        "training_num_docs": 0 if train_set is None else len(train_set.documents),
        "training_num_annotations": 0 if train_set is None else sum(1 for e in train.set.entities() if e.class_id == args.only_class_id)
    }


if __name__ == "__main__":
    train(sys.argv[1:])

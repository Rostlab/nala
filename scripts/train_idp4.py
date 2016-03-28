import os
from collections import Counter

import pycrfsuite
import shutil
from nalaf.learning.crfsuite import PyCRFSuite
from nalaf.learning.evaluators import MentionLevelEvaluator
from nalaf.preprocessing.labelers import BIEOLabeler
from nalaf.structures.data import Dataset
from nalaf.utils.annotation_readers import AnnJsonMergerAnnotationReader, AnnJsonAnnotationReader
from nalaf.utils.readers import HTMLReader
from nalaf.utils.writers import TagTogFormat

from nala.learning.postprocessing import PostProcessing
from nala.preprocessing.definers import ExclusiveNLDefiner
from nala.utils import get_prepare_pipeline_for_best_model


def read_data(n, read_base=True):
    if read_base:
        data = HTMLReader('../resources/bootstrapping/iteration_0/base/html').read()
        AnnJsonMergerAnnotationReader('../resources/bootstrapping/iteration_0/base/annjson/members',
                                      strategy='intersection', entity_strategy='priority',
                                      priority=['Ectelion', 'abojchevski', 'sanjeevkrn', 'Shpendi']).annotate(data)
    else:
        data = Dataset()

    for i in range(1, n + 1):
        try:
            tmp_data = HTMLReader('../resources/bootstrapping/iteration_{}/candidates/html'.format(i)).read()
            AnnJsonAnnotationReader('../resources/bootstrapping/iteration_{}/reviewed'.format(i),
                                    delete_incomplete_docs=False).annotate(tmp_data)
            data.extend_dataset(tmp_data)
        except FileNotFoundError:
            pass

    ExclusiveNLDefiner().define(data)
    print('read {} documents'.format(len(data)))
    print('subclass distribution:', Counter(ann.subclass for ann in data.annotations()))
    return data


# train() does the training, post-processing and printing of perfomance
def train(evaluate_on_test=True, model_name='idp4_model', delete_subclasses=[]):
    data = read_data(51, True)

    train, test = data.stratified_split()
    print('train: {}, test: {}'.format(len(train), len(test)))
    del data
    train.prune()
    train.delete_subclass_annotations(delete_subclasses)
    pipeline = get_prepare_pipeline_for_best_model()
    pipeline.execute(train)
    BIEOLabeler().label(train)

    py_crf = PyCRFSuite()
    py_crf.train(train, model_name)

    if evaluate_on_test:
        pipeline.execute(test)
        BIEOLabeler().label(test)
        py_crf.tag(test, model_name)

        PostProcessing().process(test)
        ExclusiveNLDefiner().define(test)

        exact = MentionLevelEvaluator(strictness='exact', subclass_analysis=True).evaluate(test)
        overlapping = MentionLevelEvaluator(strictness='overlapping', subclass_analysis=True).evaluate(test)

        for e in exact:
            print(e)
        for e in overlapping:
            print(e)


# test() is if you just wanna test with a pre-trained model
def test(model='idp4_model'):
    data = read_data(51, True)

    train, test = data.stratified_split()
    print('train: {}, test: {}'.format(len(train), len(test)))
    del data
    del train

    pipeline = get_prepare_pipeline_for_best_model()
    pipeline.execute(test)
    BIEOLabeler().label(test)

    py_crf = PyCRFSuite()
    py_crf.tag(test, model)

    PostProcessing().process(test)
    ExclusiveNLDefiner().define(test)

    exact = MentionLevelEvaluator(strictness='exact', subclass_analysis=True).evaluate(test)
    overlapping = MentionLevelEvaluator(strictness='overlapping', subclass_analysis=True).evaluate(test)

    for e in exact:
        print(e)
    for e in overlapping:
        print(e)


def train_and_test_2_models():
    train(False, 'idp4_model_ST', delete_subclasses=[1, 2])
    train(False, 'idp4_model_ALL3', delete_subclasses=[])

    test_2_models('idp4_model_ST', 'idp4_model_ALL3')


def test_2_models(model_1, model_2):
    data = read_data(51, True)
    train, test = data.stratified_split()
    print('train: {}, test: {}'.format(len(train), len(test)))
    del data
    del train

    # delete real annotations before exporting
    for part in test.parts():
        part.annotations = []

    pipeline = get_prepare_pipeline_for_best_model()
    pipeline.execute(test)
    BIEOLabeler().label(test)

    py_crf = PyCRFSuite()

    if os.path.exists('./2_models'):
        shutil.rmtree('./2_models')
    os.mkdir('./2_models')

    py_crf.tag(test, model_1)
    TagTogFormat(test, use_predicted=True, to_save_to='.').export_ann_json()
    os.rename('annjson', './2_models/model_1_annjson')
    for part in test.parts():
        print('ST', [ann.text for ann in part.predicted_annotations])
        part.predicted_annotations = []

    py_crf.tag(test, model_2)
    TagTogFormat(test, use_predicted=True, to_save_to='.').export_ann_json()
    os.rename('annjson', './2_models/model_2_annjson')
    shutil.rmtree('html')
    for part in test.parts():
        print('NL', [ann.text for ann in part.predicted_annotations])
        part.predicted_annotations = []

    # read in again real annotations
    data = read_data(51, True)
    train, test = data.stratified_split()
    del data
    del train

    # read in merged predictions
    AnnJsonMergerAnnotationReader('./2_models', strategy='union', entity_strategy='priority',
                                  priority=['model_1_annjson', 'model_2_annjson'],
                                  delete_incomplete_docs=False, is_predicted=True).annotate(test)
    for part in test.parts():
        print('JOINED', [ann.text for ann in part.predicted_annotations])

    PostProcessing().process(test)
    ExclusiveNLDefiner().define(test)

    exact = MentionLevelEvaluator('exact', subclass_analysis=True).evaluate(test)
    overlapping = MentionLevelEvaluator('overlapping', subclass_analysis=True).evaluate(test)

    for e in exact:
        print(e)
    for e in overlapping:
        print(e)


# evaluate() is to print out the most_common features learned
def evaluate(model='idp4_model'):
    tagger = pycrfsuite.Tagger()
    tagger.open(model)
    info = tagger.info()

    print('Transitions:')
    for (label_from, label_to), weight in Counter(info.transitions).most_common():
        print("%-6s -> %-7s %0.6f" % (label_from, label_to, weight))

    print('\nTop positive:')
    for (attr, label), weight in Counter(info.state_features).most_common(50):
        print("%0.6f %-6s %s" % (weight, label, attr))

    print("\nTop negative:")
    for (attr, label), weight in Counter(info.state_features).most_common()[-50:]:
        print("%0.6f %-6s %s" % (weight, label, attr))


if __name__ == '__main__':
    # train()
    # test()
    # evaluate()
    train_and_test_2_models()

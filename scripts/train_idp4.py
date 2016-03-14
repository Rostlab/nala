from collections import Counter

from nalaf.learning.crfsuite import PyCRFSuite
from nalaf.learning.evaluators import MentionLevelEvaluator
from nalaf.preprocessing.labelers import BIEOLabeler
from nalaf.structures.data import Dataset
from nalaf.utils.annotation_readers import AnnJsonMergerAnnotationReader, AnnJsonAnnotationReader
from nalaf.utils.readers import HTMLReader
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


def train(evaluate_on_test=True):
    data = read_data(51, True)

    train, test = data.stratified_split()
    print('train: {}, test: {}'.format(len(train), len(test)))
    del data
    train.prune()

    pipeline = get_prepare_pipeline_for_best_model()
    pipeline.execute(train)
    BIEOLabeler().label(train)

    py_crf = PyCRFSuite()
    py_crf.train(train, 'idp4_model')

    if evaluate_on_test:
        pipeline.execute(test)
        BIEOLabeler().label(test)
        py_crf.tag(test, 'idp4_model')

        PostProcessing().process(test)
        ExclusiveNLDefiner().define(test)

        MentionLevelEvaluator(strictness='exact', subclass_analysis=True).evaluate(test)
        MentionLevelEvaluator(strictness='overlapping', subclass_analysis=True).evaluate(test)


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

    MentionLevelEvaluator(strictness='exact', subclass_analysis=True).evaluate(test)
    MentionLevelEvaluator(strictness='overlapping', subclass_analysis=True).evaluate(test)


if __name__ == '__main__':
    train()

from nalaf.learning.crfsuite import PyCRFSuite
from nalaf.learning.evaluators import MentionLevelEvaluator
from nalaf.preprocessing.labelers import BIEOLabeler
from nalaf.structures.data import Dataset
from nala.learning.postprocessing import PostProcessing
from nala.preprocessing.definers import ExclusiveNLDefiner
from nala.utils import get_prepare_pipeline_for_best_model
from scripts.train_idp4 import read_data
import random
import math


def find_number_of_documents():
    data = read_data(39, read_base=False)
    train, test = data.stratified_split()
    del data
    del train

    pipeline = get_prepare_pipeline_for_best_model()
    pipeline.execute(test)
    BIEOLabeler().label(test)
    PyCRFSuite().tag(test, 'idp4_model')
    PostProcessing().process(test)
    ExclusiveNLDefiner().define(test)

    keys = test.documents.keys()
    for test_size in range(30, 101, 10):
        sample = Dataset()
        random_keys = random.sample(keys, test_size)
        sample.documents = {key: test.documents[key] for key in random_keys}

        print('============== {} =============='.format(test_size))
        calculate_standard_error(sample)


def calc_std(mean, array):
    cleaned = [n for n in array if not math.isnan(n)]
    return math.sqrt(sum((n-mean)**2 for n in cleaned)/(len(cleaned)-1))


def calculate_standard_error(data):
    evaluator = MentionLevelEvaluator('overlapping', subclass_analysis=True)
    keys = data.documents.keys()

    subclass_measures, measures = evaluator.evaluate(data)

    sample_precision = {subclass: [] for subclass in subclass_measures.keys()}
    sample_recall = {subclass: [] for subclass in subclass_measures.keys()}
    sample_f_score = {subclass: [] for subclass in subclass_measures.keys()}

    for i in range(1000):
        sample = Dataset()
        random_keys = random.sample(keys, round(len(keys)*0.15))
        sample.documents = {key: data.documents[key] for key in random_keys}

        subclass_measures, measures = evaluator.evaluate(sample)

        for subclass in subclass_measures.keys():
            subclass_results = subclass_measures[subclass]
            sample_precision[subclass].append(subclass_results[-3])
            sample_recall[subclass].append(subclass_results[-2])
            sample_f_score[subclass].append(subclass_results[-1])

    for subclass in subclass_measures.keys():
        subclass_results = subclass_measures[subclass]
        mean_precision = subclass_results[-3]
        mean_recall = subclass_results[-2]
        mean_f_score = subclass_results[-1]

        p = calc_std(mean_precision, sample_precision[subclass])
        r = calc_std(mean_recall, sample_recall[subclass])
        f = calc_std(mean_f_score, sample_f_score[subclass])

        print('subclass:{} {:.4f}+-{:.4f} {:.4f}+-{:.4f} {:.4f}+-{:.4f}'.format(
            subclass, mean_precision, p, mean_recall, r, mean_f_score, f
        ))


find_number_of_documents()
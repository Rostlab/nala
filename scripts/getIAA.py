from nalaf.utils.annotation_readers import AnnJsonAnnotationReader
from nalaf.learning.evaluators import MentionLevelEvaluator
from itertools import combinations
import os
from nalaf.structures.data import Dataset
from nala.bootstrapping.iteration import IterationRound
from nala.preprocessing.definers import ExclusiveNLDefiner

members=['abojchevski', 'jmcejuela', 'cuhlig']

def benchmark(member1, member2):
    dataset = Dataset()
    for itr in IterationRound.all():
        if itr.is_IAA():
            dataset.extend_dataset(itr.read(read_annotations = False))
            AnnJsonAnnotationReader(os.path.join(itr.path, "reviewed", member1), delete_incomplete_docs = False).annotate(dataset)
            AnnJsonAnnotationReader(os.path.join(itr.path, "reviewed", member2), delete_incomplete_docs = False, is_predicted=True).annotate(dataset)

    ExclusiveNLDefiner().define(dataset)

    exact = MentionLevelEvaluator(strictness = 'exact', subclass_analysis=True).evaluate(dataset)
    overlapping = MentionLevelEvaluator(strictness = 'overlapping', subclass_analysis=True).evaluate(dataset)
    return exact, overlapping

for member1, member2 in combinations(members, 2):
    print(member1, member2)
    exact, overlapping = benchmark(member1, member2)

    for e in exact:
        print(e)
    for e in overlapping:
        print(e)

    print("")
from nalaf.utils.annotation_readers import AnnJsonAnnotationReader
from nalaf.learning.evaluators import MentionLevelEvaluator
from itertools import combinations
import os
import sys
from nalaf.structures.data import Dataset
from nala.bootstrapping.iteration import IterationRound
from nala.preprocessing.definers import ExclusiveNLDefiner

IDP4_members = ['Ectelion', 'abojchevski', 'sanjeevkrn', 'Shpendi']
nala_members = ['cuhlig', 'abojchevski', 'jmcejuela']

def benchmark_IDP4(member1, member2):
    dataset = Dataset()
    itr = IterationRound(0)
    dataset.extend_dataset(itr.read(read_annotations = False))
    AnnJsonAnnotationReader(os.path.join(itr.path, "base", "annjson", "members", member1), delete_incomplete_docs = True).annotate(dataset)
    AnnJsonAnnotationReader(os.path.join(itr.path, "base", "annjson", "members", member1), delete_incomplete_docs = True, is_predicted=True).annotate(dataset)

    print(dataset.__repr__())

    ExclusiveNLDefiner().define(dataset)

    exact = MentionLevelEvaluator(strictness = 'exact', subclass_analysis=True).evaluate(dataset)
    overlapping = MentionLevelEvaluator(strictness = 'overlapping', subclass_analysis=True).evaluate(dataset)
    return exact, overlapping

def benchmark_nala(member1, member2):
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

if sys.argv[1] == "IDP4":
    members = IDP4_members
    benchmark = benchmark_IDP4
else:
    members = nala_members
    benchmark = benchmark_nala

for member1, member2 in combinations(members, 2):
    print(member1, member2)
    exact, overlapping = benchmark(member1, member2)

    for e in exact:
        print(e)
    for e in overlapping:
        print(e)

    print("")

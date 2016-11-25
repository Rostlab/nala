from nalaf.utils.annotation_readers import AnnJsonAnnotationReader
from nalaf.learning.evaluators import MentionLevelEvaluator, Evaluations
from itertools import combinations
import os
import sys
from nalaf.structures.data import Dataset
from nala.bootstrapping.iteration import IterationRound
from nala.preprocessing.definers import ExclusiveNLDefiner
from nala.utils import MUT_CLASS_ID, PRO_CLASS_ID


IDP4_members = ['Ectelion', 'abojchevski', 'sanjeevkrn', 'Shpendi']
nala_members = ['cuhlig', 'abojchevski', 'jmcejuela']

IDP4_IAA_docs = [
    "23144459",
    "9287304",
    "17728323",
    "9113409",
    "15546125",
    "6488317",
    "7559441",
    "9502794",
    "9688573",
    "12663043",
    "15718227",
    "12560877",
    "17327381",
    "15201367",
    "16621600",
    "10080891",
    "9026534",
    "PMC3244487",
    "15231984",
    "10454540",
    "7893703",
    "15015733",
    "8420982",
    "7912128",
    "PMC1143697",
    "9514978",
    "12019207",
    "PMC3464205",
    "7488859",
    "9101292",
    "PMC2233692",
    "8655141",
    "10843183",
    "PMC3815127",
    "8162033",
    "18199800",
    "9448270",
    "8013629",
    "10747788",
    "18179891",
    "18319072",
    "PMC31919",
    "11684697",
    "14576201",
    "11342563",
    "17468127",
    "PMC3030776",
    "14672928",
    "12559908",
    "PMC3668507",
    "9916143",
    "nar_gkp166",
    "ng.1091"
]

def benchmark_IDP4(member1, member2):
    itr = IterationRound(0)
    IDP4_corpus = itr.read(read_annotations=False)

    IAA_IDP4_corpus = Dataset()
    for docid, document in IDP4_corpus.documents.items():
        if docid in IDP4_IAA_docs:
            IAA_IDP4_corpus.documents[docid] = document

    AnnJsonAnnotationReader(os.path.join(itr.path, "base", "annjson", "members", member1), read_only_class_id=MUT_CLASS_ID, delete_incomplete_docs=True).annotate(IAA_IDP4_corpus)
    AnnJsonAnnotationReader(os.path.join(itr.path, "base", "annjson", "members", member2), read_only_class_id=MUT_CLASS_ID, delete_incomplete_docs=True, is_predicted=True).annotate(IAA_IDP4_corpus)

    ExclusiveNLDefiner().define(IAA_IDP4_corpus)

    return (IAA_IDP4_corpus, MentionLevelEvaluator(subclass_analysis=True).evaluate(IAA_IDP4_corpus))


def benchmark_nala(member1, member2):
    itrs = []

    # Read the IAA iterations in blocks so that the plain documents are not deleted with the AnnJsonAnnotationReader's
    for itr in IterationRound.all():
        if itr.is_IAA():
            dataset = itr.read(read_annotations=False)
            AnnJsonAnnotationReader(os.path.join(itr.path, "reviewed", member1), read_only_class_id=MUT_CLASS_ID, delete_incomplete_docs=False).annotate(dataset)
            AnnJsonAnnotationReader(os.path.join(itr.path, "reviewed", member2), read_only_class_id=MUT_CLASS_ID, delete_incomplete_docs=False, is_predicted=True).annotate(dataset)
            itrs.append(dataset)
            dataset = None

    # Then merge the IAA iterations
    all_itrs_dataset = Dataset()
    for itr_dataset in itrs:
        all_itrs_dataset.extend_dataset(itr_dataset)

    ExclusiveNLDefiner().define(all_itrs_dataset)

    return (all_itrs_dataset, MentionLevelEvaluator(subclass_analysis=True).evaluate(all_itrs_dataset))


# ---


if sys.argv[1] == "IDP4":
    members = IDP4_members
    benchmark = benchmark_IDP4
else:
    members = nala_members
    benchmark = benchmark_nala

show_only_total_results = True if len(sys.argv) > 2 and sys.argv[2] == "only_total" else False

# ---

total_dataset = Dataset()
individual_evaluations = []

for member1, member2 in combinations(members, 2):
    (dataset, evaluation) = benchmark(member1, member2)

    if not show_only_total_results:
        print(member1, member2)
        print("  -> Overlapping: ", dataset.__repr__())
        print(evaluation)
        print("")
        individual_evaluations.append(evaluation)

    total_dataset.extend_dataset(dataset)
    dataset = None
    evaluation = None


total_evaluation = Evaluations.merge(individual_evaluations, are_disjoint_evaluations=False)

print()
print()
print("_Total_ overlapping: ", total_dataset.__repr__(), ", num members pairs: ", len(individual_evaluations))
print()
print(total_evaluation)

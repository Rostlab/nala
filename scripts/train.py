import argparse
import os
import tempfile
from collections import Counter
from nala.preprocessing.definers import ExclusiveNLDefiner
from nala.utils.corpora import get_corpus
from nalaf.preprocessing.labelers import BIEOLabeler
from nala.utils import get_prepare_pipeline_for_best_model
from nalaf.learning.crfsuite import PyCRFSuite
from nalaf.learning.evaluators import MentionLevelEvaluator
from nala.learning.taggers import NalaSingleModelTagger, NalaTagger

parser = argparse.ArgumentParser(description='Print corpora stats')

group1 = parser.add_mutually_exclusive_group(required=True)

group1.add_argument('--training_corpus',
    help='Name of the corpus to train on. Examples: IDP4+, nala_training, IDP4+_training, nala_training_5')
group1.add_argument('--test_corpus',
    help='Name of the corpus to test on')

parser.add_argument('--model_name', required = False,
    help='Name of the model to create if training is performed')
parser.add_argument('--model_path_1', required = False,
    help='Path of the first model binary file if evaluation is performed')
parser.add_argument('--model_path_2', required = False,
    help='Path of the second model binary file if evaluation is performed with two models')

parser.add_argument('--delete_subclasses', required = False, default = "",
    help='Comma-separated subclasses to delete. Example: "2,3"')
parser.add_argument('--elastic_net', action='store_true',
    help='Use elastic net regularization')
parser.add_argument('--word_embeddings', action='store_false',
    help='Do not use word embeddings. On by default')

args = parser.parse_args()

delete_subclasses = []
for c in args.delete_subclasses:
    c.strip()
    if c:
        delete_subclasses.append(int(c))

args.delete_subclasses = delete_subclasses

args.tmpdir = tempfile.mkdtemp()
if not args.model_name:
    args.model_name = args.training_corpus

args.do_train = False if args.model_path_1 else True

print("Running arguments: ")
for key, value in sorted((vars(args)).items()):
    print("\t{} = {}".format(key, value))
print()

#------------------------------------------------------------------------------

features_pipeline = get_prepare_pipeline_for_best_model(use_word_embeddings = args.word_embeddings)

#------------------------------------------------------------------------------

def stats(dataset, name):
    print('\n{} size: {}'.format(name, len(dataset)))
    print('\tsubclass distribution: {}\n\n'.format(Counter(ann.subclass for ann in dataset.annotations())))

def train(train_set):
    train_set.prune()
    ExclusiveNLDefiner().define(train_set)
    stats(train_set, "training")

    train_set.delete_subclass_annotations(args.delete_subclasses)
    features_pipeline.execute(train_set)
    BIEOLabeler().label(train_set)

    if args.elastic_net:
        params = {
            'c1': 1.0, # coefficient for L1 penalty
            'c2': 1e-3, # coefficient for L2 penalty
        }
    else:
        params = None

    crf = PyCRFSuite()

    model_path = os.path.join(args.tmpdir, args.model_name + ".bin")
    crf.train(train_set, model_path, params)

    return model_path

if args.training_corpus:
    train_set = get_corpus(args.training_corpus)
    ExclusiveNLDefiner().define(train_set)
    train_set, test_set = train_set.stratified_split()
else:
    train_set = test_set = None

if args.do_train:
    args.model_path_1 = train(train_set)

#------------------------------------------------------------------------------

def test(tagger, test_set):
    tagger.tag(test_set)

    ExclusiveNLDefiner().define(test_set)
    stats(test_set, "test")
    exact = MentionLevelEvaluator(strictness='exact', subclass_analysis=True).evaluate(test_set)
    overlapping = MentionLevelEvaluator(strictness='overlapping', subclass_analysis=True).evaluate(test_set)

    print("\n{}\n".format(args.training_corpus))

    for e in exact:
        print(e)
    print()
    for e in overlapping:
        print(e)
    print()

assert(args.model_path_1 is not None)

if args.model_path_2:
    tagger = NalaTagger(st_model = args.model_path_1, all3_model = args.model_path_2, features_pipeline = features_pipeline)
else:
    tagger = NalaSingleModelTagger(bin_model = args.model_path_1, features_pipeline = features_pipeline)

if test_set is None:
    test_set = get_corpus(args.test_corpus)

test(tagger, test_set)

if args.do_train:
    print("\nThe model is saved to: {}\n".format(args.model_path_1))

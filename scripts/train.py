import argparse
import os
import tempfile
from nala.preprocessing.definers import ExclusiveNLDefiner
from nala.utils.corpora import get_corpus
from nalaf.preprocessing.labelers import BIEOLabeler
from nala.utils import get_prepare_pipeline_for_best_model
from nalaf.learning.crfsuite import PyCRFSuite

from nalaf.learning.evaluators import MentionLevelEvaluator
from nala.learning.taggers import NalaSingleModelTagger

parser = argparse.ArgumentParser(description='Print corpora stats')

parser.add_argument('--model_name', required = True,
    help='Name of the model to create')
parser.add_argument('--training_corpus', required = True,
    help='Name of the corpus to train on. Examples: IDP4+, nala_training, IDP4+_training, nala_training_5')
parser.add_argument('--test_corpus', required = True,
    help='Name of the corpus test test on; special values `stratified` or `cross validation` to test on the train corpus')
parser.add_argument('--delete_classes', required = False, default = "",
    help='Comma-separated subclasses to delete. Example: "2,3"')
parser.add_argument('--elastic_net', action='store_true',
    help='Use elastic net regularization')
parser.add_argument('--word_embeddings', action='store_false',
    help='Use word embeddings')

args = parser.parse_args()

delete_classes = []
for c in args.delete_classes:
    c.strip()
    if c:
        delete_classes.append(int(c))

args.delete_classes = delete_classes

args.tmpdir = tempfile.mkdtemp()
args.model_path = os.path.join(args.tmpdir, args.model_name + ".bin")

print("Running arguments: ")
for arg in args:
    print(arg)
print()

#------------------------------------------------------------------------------

train_set = get_corpus(args.training_corpus)

if args.test_corpus == "stratified":
    train_set, test_set = train_set.stratified_split()
elif args.test_corpus == "cross validation":
    raise Exception("Cross Validation not supported yet")
else:
    test_set = get_corpus(args.test_corpus)

ExclusiveNLDefiner().define(train_set)
train_set.delete_subclass_annotations(args.delete_subclasses)

ExclusiveNLDefiner().define(test_set)
test_set.delete_subclass_annotations(args.delete_subclasses)

print('trainining size: {}, test size: {}'.format(len(train_set), len(test_set)))

# TRAIN

train_set.prune()
pipeline = get_prepare_pipeline_for_best_model(use_word_embeddings = args.word_embeddings)
pipeline.execute(train_set)
BIEOLabeler().label(train_set)

if args.elastic_net:
    params = {
        'c1': 1.0, # coefficient for L1 penalty
        'c2': 1e-3, # coefficient for L2 penalty
    }
else:
    params = None

crf = PyCRFSuite()

crf.train(train_set, args.model_path, params)

tagger = NalaSingleModelTagger(bin_model = args.model_path, features_pipeline = pipeline)

# TEST

tagger.tag(test_set)

exact = MentionLevelEvaluator(strictness='exact', subclass_analysis=True).evaluate(test_set)
overlapping = MentionLevelEvaluator(strictness='overlapping', subclass_analysis=True).evaluate(test_set)

for e in exact:
    print(e)

print()

for e in overlapping:
    print(e)

print()
print("The model is saved to: {}".format(args.model_path))

import argparse

from nala.preprocessing.definers import ExclusiveNLDefiner
from nala.utils.corpora import get_corpus, ALL_CORPORA
from nalaf.utils import MUT_CLASS_ID
from nalaf.structures.dataset_pipelines import PrepareDatasetPipeline
from nalaf.structures.data import Dataset

parser = argparse.ArgumentParser(description='Print corpora stats')

parser.add_argument('corpora', default='*', metavar='corpus', nargs='+',
                    help='Name of the corpus to read and print stats for')
parser.add_argument('--listanns', default="",
                    help='Print mutation comma-separated subclasses. Examples: 1 or 1,2 or * for all')
parser.add_argument('--counttokens', help='Count the tokens. Note, this is considerably slower', action='store_true')
parser.add_argument('--test', help='Get the test (sub)set if any, otherwise the entire corpus', action='store_true')

args = parser.parse_args()

if args.corpora[0] == "*" or args.corpora[0] == 'all':
    args.corpora = ALL_CORPORA

if args.listanns == '*' or args.listanns == 'all':
    args.listanns = '0,1,2'
args.listanns = set(int(c) for c in args.listanns.split(",") if c)

# ------------------------------------------------------------------------------

nldefiner = ExclusiveNLDefiner()

pipeline = PrepareDatasetPipeline(feature_generators=[])

ST = 0  # Standard
NL = 1  # Natural Language
SS = 2  # Semi-Standard

# ------------------------------------------------------------------------------

def get_corpus_type(name):
    if name == "MF":
        return (name, None)
    elif name.endswith("A"):
        return (name[:-1], "A")
    elif name.endswith("F"):
        return (name[:-1], "F")
    else:
        return (name, None)

def is_part_type(part, typ):
    return not typ or (typ == "A" and part.is_abstract) or (typ == "F" and not part.is_abstract)

def is_abstract_only(document):
    return all(part.is_abstract for part in document)

def is_full_text(document):
    return any(not part.is_abstract for part in document)

def annotations(corpus, typ):
    nldefiner.define(corpus)  # classify subclasses

    for docid, document in corpus.documents.items():
        for part in document:
            if is_part_type(part, typ):
                for annotation in part.annotations:
                    yield annotation

def get_num_tokens(corpus, typ):
    if (args.counttokens):
        pipeline.execute(corpus) # obtain tokens

        ret = 0
        for part in corpus.parts():
            if is_part_type(part, typ):
                for sentence in part.sentences:
                    ret += len(sentence)

        return ret
    else:
        return -1

def filter_only_full_text(corpus):
    newcorpus = Dataset()
    for docid, document in corpus.documents.items():
        if is_full_text(document):
            newcorpus.documents[docid] = document

    return newcorpus

header = ["Corpus", "#docs", "#ann", "#ST", "%ST", "#NL", "%NL", "#SS", "%SS", "#NL+SS", "%NL+SS", "#tokens"]

def print_stats(name, corpus, typ):
    corpus = filter_only_full_text(corpus) if typ == "F" else corpus
    total = 0
    counts = [0, 0, 0]
    marker = [
        '',
        '@@@@@@@@@@@@@@@@@@@@@@',
        '**********************'
    ]

    for ann in annotations(corpus, typ):
        if ann.class_id == MUT_CLASS_ID:
            if ann.subclass in args.listanns:
                print('\t', ann.subclass, ann.text, marker[ann.subclass], sep='\t')
            total += 1
            counts[ann.subclass] += 1

    num_tokens = get_num_tokens(corpus, typ)

    fs = "{0:.3f}"
    percents = list(map(lambda x: (fs.format(x / total) if x > 0 else "0"), counts))

    # if (args.listall):
    #     print('\t'.join(header))

    # The limit of 7 for the corpus name is the size that fits into a tab column, so that it looks good on print
    values = [name[:7], len(corpus.documents), total, counts[ST], percents[ST], counts[NL], percents[NL], counts[SS], percents[SS], (counts[NL] + counts[SS]), "{0:.3f}".format(1 - float(percents[ST])), num_tokens]
    print(*values, sep='\t')

#------------------------------------------------------------------------------

print('\t'.join(header))

for corpus_name in args.corpora:
    realname, typ = get_corpus_type(corpus_name)
    corpus = get_corpus(realname, args.test)
    print_stats(corpus_name, corpus, typ)

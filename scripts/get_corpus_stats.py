import argparse

from nala.preprocessing.definers import ExclusiveNLDefiner
from nala.utils.corpora import get_corpus, ALL_CORPORA
from nala.utils import MUT_CLASS_ID
from nalaf.structures.dataset_pipelines import PrepareDatasetPipeline
from nalaf.structures.data import Dataset
# from collections import Counter

parser = argparse.ArgumentParser(description='Print corpora stats')

parser.add_argument('corpora', default='*', metavar='corpus', nargs='+',
                    help='Name of the corpus to read and print stats for')
parser.add_argument('--listanns', default="",
                    help='Print mutation comma-separated subclasses. Examples: 1 or 1,2 or * for all')
parser.add_argument('--counttokens', help='Count the tokens. Note, this is considerably slower', action='store_true')

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

MARKER = [
    '        ',
    '@@@@@@@@',
    '********'
]

PROB = "{0:.3f}"  # FORMAT

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

def corpus_annotations(corpus, typ):
    for docid, document in corpus.documents.items():
        for part in document:
            if is_part_type(part, typ):
                for annotation in part.annotations:
                    yield annotation

def doc_annotations(document, typ):
    for part in document:
        if is_part_type(part, typ):
            for annotation in part.annotations:
                yield annotation

def get_num_tokens(corpus, typ):
    if (args.counttokens):
        pipeline.execute(corpus)  # obtain tokens

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


# WordsCounter = Counter()

def get_stats(name, corpus, typ):
    nldefiner.define(corpus)  # classify subclasses

    corpus = filter_only_full_text(corpus) if typ == "F" else corpus
    num_muts = 0
    counts = [0, 0, 0]

    num_docs_with_NL = 0
    num_docs_with_NL_untraslated = 0
    num_NLs_untranslated = 0

    for docid, document in corpus.documents.items():
        doc_has_NL = False
        docs_num_NL = 0

        for ann in doc_annotations(document, typ):
            if ann.class_id == MUT_CLASS_ID:
                num_muts += 1
                counts[ann.subclass] += 1

                if ann.subclass == NL:
                    doc_has_NL = True
                    docs_num_NL += 1

                if ann.subclass in args.listanns:
                    print('\t' + '#' + str(num_muts) + '  ' + str(ann.subclass) + ' ' + MARKER[ann.subclass] + ' : ' + ann.text)

                # for word in ann.text.split(' '):
                #     WordsCounter[word.lower()] += 1

        if doc_has_NL:
            num_docs_with_NL += 1

            num_relations = len(list(document.relations()))
            # This is a simplification and pesimistic estimation. The relations could be between NLs or involve a lower number of NLs
            untranslated = num_relations == 0

            if untranslated:
                num_docs_with_NL_untraslated += 1
                num_NLs_untranslated += docs_num_NL

    num_docs = len(corpus.documents)
    num_tokens = get_num_tokens(corpus, typ)
    percents = list(map(lambda x: (PROB.format(x / num_muts) if x > 0 else "0"), counts))
    per_docs_with_NL_untraslated = PROB.format(num_docs_with_NL_untraslated / num_docs)
    per_NLs_untraslated = PROB.format(num_NLs_untranslated / num_muts)

    # if (args.listall):
    #     print('\t'.join(header))

    # The limit of 7 for the corpus name is the size that fits into a tab column, so that it looks good on print
    return [
        name[:7],
        num_docs,
        num_tokens,
        num_muts,
        counts[ST],
        percents[ST],
        counts[NL],
        percents[NL],
        counts[SS],
        percents[SS],
        (counts[NL] + counts[SS]),
        PROB.format(1 - float(percents[ST])),
        per_docs_with_NL_untraslated,
        per_NLs_untraslated
    ]

# ------------------------------------------------------------------------------

# %d_u_NL == percentage of documents that have at least one untranslated NL mention
# %m_u_NL == percentage of mentions that are NL and are untranslated to ST
header = ["Corpus", "#docs", "#tokens", "#ann", "#ST", "%ST", "#NL", "%NL", "#SS", "%SS", "#NL+SS", "%NL+SS", "%d_u_NL", "%m_u_NL"]

print('\t'.join(header))

for corpus_name in args.corpora:
    realname, typ = get_corpus_type(corpus_name)
    corpus = get_corpus(realname)
    columns = get_stats(corpus_name, corpus, typ)
    if args.listanns:
        print('\t'.join(header))
    print(*columns, sep='\t')

# for count in WordsCounter.most_common()[:-len(WordsCounter)-1:-1]:
#     print(count)

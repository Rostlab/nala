import argparse
import os
from nala.bootstrapping.iteration import Iteration
from nala.preprocessing.definers import ExclusiveNLDefiner
from nalaf.utils.readers import VerspoorReader, TmVarReader, SETHReader
from nalaf.utils.annotation_readers import SETHAnnotationReader
from nalaf.utils import MUT_CLASS_ID
from nalaf.structures.dataset_pipelines import PrepareDatasetPipeline
from nalaf.structures.data import Dataset


parser = argparse.ArgumentParser(description='Print corpora stats')

#Var = Variome
#Var120 = Variome_120
#?A = Abstracts only
#?F = Full Text only
all_corpora = [
'tmVar', 'MF', 'SETH', 'OMM', 'OSIRIS', 'SNPC',
'IDP4', 'IDP4A', 'IDP4F', 'nala', 'IDP4+',
'Var', 'VarA', 'VarF', 'Var120', 'Var120A', 'Var120F']

parser.add_argument('--corpus', help='Name of the corpus to read and print stats for', required = True)
parser.add_argument('--listall', help='Print mutations', action='store_true')
parser.add_argument('--counttokens', help='Count the tokens. Note that this is considerably slower', action='store_true')

args = parser.parse_args()

#------------------------------------------------------------------------------

corpora_folder = os.path.abspath("resources/corpora")

nldefiner = ExclusiveNLDefiner()

pipeline = PrepareDatasetPipeline()

ST = 0 #Standard
NL = 1 #Natural Language
SS = 2 #Semi-Standard

#------------------------------------------------------------------------------



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
    nldefiner.define(corpus) # classify subclasses

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

def get_corpus(name):
    if name == "tmVar":
        entirecorpusfile = os.path.join(corpora_folder, 'tmvar', 'corpus.txt')
        return TmVarReader(entirecorpusfile).read()
    if name == "SETH":
        ret = SETHReader(os.path.join(corpora_folder, 'seth', 'corpus.txt')).read()
        annreader = SETHAnnotationReader(os.path.join(corpora_folder, 'seth', 'annotations'))
        annreader.annotate(ret)
        return ret
    elif name == "IDP4":
        return Iteration.read_IDP4()
    elif name == "nala":
        return Iteration.read_nala()
    elif name == "IDP4+":
        return Iteration.read_IDP4Plus()
    elif name == "Var":
        folder = os.path.join(corpora_folder, 'variome', 'data')
        return VerspoorReader(folder).read()
    elif name == "Var120":
        folder = os.path.join(corpora_folder, 'variome_120', 'annotations_mutations_explicit')
        return VerspoorReader(folder).read()
    elif name in all_corpora:
        return Dataset()
        #raise NotImplementedError("My bad, not implemented: " + name)
    else:
        raise Exception("Do not recognize given corpus name: " + name)

header = ["Corpus", "#docs", "#ann", "#ST", "%ST", "#NL", "%NL", "#SS", "%SS", "#NL+SS", "%NL+SS", "#tokens"]

def print_stats(name, corpus, typ):
    corpus = filter_only_full_text(corpus) if typ == "F" else corpus
    total = 0
    counts = [0,0,0]

    for ann in annotations(corpus, typ):
        if ann.class_id == MUT_CLASS_ID:
            if (args.listall):
                print('\t', ann.subclass, ann.text, sep = '\t')
            total += 1
            counts[ann.subclass] += 1

    num_tokens = get_num_tokens(corpus, typ)

    fs = "{0:.3f}"
    percents = list(map(lambda x: (fs.format(x / total) if x > 0 else "0"), counts))

    if (args.listall):
        print('\t'.join(header))

    values = [name, len(corpus.documents), total, counts[ST], percents[ST], counts[NL], percents[NL], counts[SS], percents[SS], (counts[NL] + counts[SS]), "{0:.3f}".format(1 - float(percents[ST])), num_tokens]
    print(*values, sep = '\t')

#------------------------------------------------------------------------------

print('\t'.join(header))

if args.corpus == "*" or args.corpus == "all":
    for corpus_name in all_corpora:
        realname, typ = get_corpus_type(corpus_name)
        corpus = get_corpus(realname)
        print_stats(corpus_name, corpus, typ)

else:
    realname, typ = get_corpus_type(args.corpus)
    corpus = get_corpus(realname)
    print_stats(args.corpus, corpus, typ)

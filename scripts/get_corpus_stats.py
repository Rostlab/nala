import argparse
import os
from nala.bootstrapping.iteration import Iteration
from nala.preprocessing.definers import ExclusiveNLDefiner
from nalaf.utils.readers import VerspoorReader
from nalaf.utils import MUT_CLASS_ID


parser = argparse.ArgumentParser(description='Print corpora stats')

#Var = Variome
#Var120 = Variome_120
#?A = Abstracts only
#?F = Full Text only
all_corpora = ['IDP4', 'IDP4A', 'IDP4F', 'nala', 'IDP4+', 'Var', 'VarA', 'VarF', 'Var120', 'Var120A', 'Var120F']

parser.add_argument('--corpus', help='Name of the corpus to read and print stats for', required = True)
parser.add_argument('--listall', help='Print mutations', action='store_true')

args = parser.parse_args()

#------------------------------------------------------------------------------

corpora_folder = os.path.abspath("resources/corpora")

#------------------------------------------------------------------------------

ST = 0 #Standard
NL = 1 #Natural Language
SS = 2 #Semi-Standard

def get_corpus_type(name):
    if name.endswith("A"):
        return (name[:-1], "A")
    if name.endswith("F"):
        return (name[:-1], "F")
    else:
        return (name, None)

def annotations(dataset, typ):
    for part in dataset.parts():
        if not typ or (typ == "A" and part.is_abstract) or (typ == "F" and not part.is_abstract):
            for annotation in part.annotations:
                yield annotation

def get_corpus(name):
    if name == "IDP4":
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
    else:
        raise Exception("Do not recognize given corpus name: " + name)

header = ["Corpus", "#docs", "#ann", "#ST", "%ST", "#NL", "%NL", "#SS", "%SS", "#NL+SS", "%NL+SS"]

def print_stats(name, corpus, typ):
    total = 0
    counts = [0,0,0]

    ExclusiveNLDefiner().define(corpus)
    for ann in annotations(corpus, typ):
        if ann.class_id == MUT_CLASS_ID:
            if (args.listall):
                print('\t', ann.subclass, ann.text, sep = '\t')
            total += 1
            counts[ann.subclass] += 1

    fs = "{0:.3f}"
    percents = list(map(lambda x: (fs.format(x / total)), counts))

    if (args.listall):
        print('\t'.join(header))

    values = [name, len(corpus.documents), total, counts[ST], percents[ST], counts[NL], percents[NL], counts[SS], percents[SS], (counts[NL] + counts[SS]), "{0:.3f}".format(1 - float(percents[ST]))]
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

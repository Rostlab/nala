import argparse
from nala.bootstrapping.iteration import Iteration
from nala.preprocessing.definers import ExclusiveNLDefiner

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Print corpora stats')

    all_corpora = ['IDP4', 'nala', 'IDP4+']

    parser.add_argument('--corpus', help='Name of the corpus to read and print stats for', required = True)
    parser.add_argument('--listall', help='Print mutations', action='store_true')

    args = parser.parse_args()

#------------------------------------------------------------------------------

ST = 0 #Standard
NL = 1 #Natural Language
SS = 2 #Semi-Standard

def get_corpus(name):
    if name == "IDP4":
        corpus = Iteration.read_IDP4()
    elif name == "nala":
        corpus = Iteration.read_nala()
    elif name == "IDP4+":
        corpus = Iteration.read_IDP4Plus()
    else:
        raise Exception("Do not recognize given corpus name: " + name)

    return corpus

def print_stats(name, corpus):
    total = 0
    counts = [0,0,0]

    ExclusiveNLDefiner().define(corpus)
    for ann in corpus.annotations():
        if (args.listall):
            print('\t', ann.subclass, ann.text, sep = '\t')
        total += 1
        counts[ann.subclass] += 1

    fs = "{0:.3f}"
    percents = list(map(lambda x: (fs.format(x / total)), counts))

    values = [name, len(corpus.documents), total, counts[ST], percents[ST], counts[NL], percents[NL], counts[SS], percents[SS], (counts[NL] + counts[SS])]

    print(*values, sep = '\t')

#------------------------------------------------------------------------------

header = ["Corpus", "#docs", "#ann", "#ST", "%ST", "#NL", "%NL", "#SS", "%SS", "#NL+SS"]
print('\t'.join(header))

if args.corpus == "*" or args.corpus == "all":
    for corpus_name in all_corpora:
        corpus = get_corpus(corpus_name)
        print_stats(corpus_name, corpus)

else:
    corpus = get_corpus(args.corpus)
    print_stats(args.corpus, corpus)

import argparse
from nala.bootstrapping.iteration import Iteration
from nala.preprocessing.definers import ExclusiveNLDefiner

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Print corpora stats')

    parser.add_argument('--dataset', help='Name of the dataset to read and print stats for')

    args = parser.parse_args()

dataset = None

#------------------------------------------------------------------------------

def print_stats(name, dataset):
    counts=[0,0,0]

    ExclusiveNLDefiner().define(dataset)
    for ann in dataset.annotations():
        counts[ann.subclass] += 1

    print(name, '#docs:', len(dataset.documents), 'ST:', counts[0], 'NL:', counts[1], 'SS:', counts[2], 'NL+SS:', counts[1] + counts[2])


#------------------------------------------------------------------------------

if args.dataset == "IDP4":
    dataset = Iteration.read_IDP4()
elif args.dataset == "nala":
    dataset = Iteration.read_nala()
elif args.dataset == "IDP4+":
    dataset = Iteration.read_IDP4Plus()
else:
    raise Exception("Do not recognize given dataset name: " + args.dataset)

print_stats(args.dataset, dataset)

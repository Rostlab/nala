import os
from nala.utils import nala_repo_path
from nala.bootstrapping.iteration import Iteration
from nalaf.utils.readers import VerspoorReader, TmVarReader, SETHReader, OSIRISReader
from nalaf.utils.annotation_readers import SETHAnnotationReader, BRATPartsAnnotationReader
from nalaf.structures.data import Dataset

# Var = Variome
# Var120 = Variome_120
# ?A = Abstracts only
# ?F = Full Text only
ALL_CORPORA = [
    'tmVar', 'MF', 'SETH', 'OMM', 'OSIRIS', 'SNP',
    'IDP4', 'IDP4A', 'IDP4F',
    'nala', 'nala_training',  # 'nala_test', activate once we are done
    'IDP4+',
    'Var', 'VarA', 'VarF', 'Var120', 'Var120A', 'Var120F']

__corpora_folder = nala_repo_path(["resources", "corpora"])

def get_corpus(name, training=False, test=False):
    parts = name.split("_")
    if len(parts) > 1:
        name = parts[0]
        training = True if parts[1] == "training" else False
        test = True if parts[1] == "test" else False
        until_iteration = int(parts[2]) if len(parts) > 2 else None

    if name == "tmVar":
        fn = 'test.PubTator.txt' if test else 'corpus.txt'
        entirecorpusfile = os.path.join(__corpora_folder, 'tmvar', fn)
        return TmVarReader(entirecorpusfile).read()

    if name == "SETH":
        ret = SETHReader(os.path.join(__corpora_folder, 'seth', 'corpus.txt')).read()
        annreader = SETHAnnotationReader(os.path.join(__corpora_folder, 'seth', 'annotations'))
        annreader.annotate(ret)
        return ret

    elif name == "IDP4":
        return Iteration.read_IDP4()

    elif name == "nala":
        if training:
            return Iteration.read_nala_training(until_iteration)
        elif test:
            return Iteration.read_nala_test()
        else:
            return Iteration.read_nala()

    elif name == "IDP4+":
        if training:
            return Iteration.read_IDP4Plus_training(until_iteration)
        elif test:
            return Iteration.read_IDP4Plus_test()
        else:
            return Iteration.read_IDP4Plus()

    elif name == "Var":
        folder = os.path.join(__corpora_folder, 'variome', 'data')
        return VerspoorReader(folder).read()

    elif name == "Var120":
        folder = os.path.join(__corpora_folder, 'variome_120', 'annotations_mutations_explicit')
        return VerspoorReader(folder).read()

    elif name == "OSIRIS":
        file = os.path.join(__corpora_folder, 'osiris', 'OSIRIScorpusv01.xml')
        return OSIRISReader(file).read()

    elif name in ALL_CORPORA:
        return Dataset()
        #raise NotImplementedError("My bad, not implemented: " + name)

    else:
        raise Exception("Do not recognize given corpus name: " + name)

import sys
import os
import subprocess
from subprocess import CalledProcessError
from nala.utils.corpora import get_corpus
from nalaf.utils.annotation_readers import SETHAnnotationReader, BRATPartsAnnotationReader
from nalaf.learning.evaluators import MentionLevelEvaluator
from nala.preprocessing.definers import ExclusiveNLDefiner

def run_seth_on_corpus(corpus, folder, useMutationFinderOnly):
    counter = 0
    for docid, document in corpus.documents.items():
        counter += 1
        print(counter, docid)
        for partid, part in document.parts.items():
            print('\t', partid)
            run_seth_on_string(part.text, docid, partid, folder, useMutationFinderOnly)

def run_seth_on_string(text, docid, partid, folder, useMutationFinderOnly):
    filename = "{}/{}-{}.ann".format(folder, docid, partid)
    run_seth_on_string_with_filename(text, filename, useMutationFinderOnly)

def run_seth_on_string_with_filename(text, filename, useMutationFinderOnly):
    try:
        with open(filename, "w") as outfile:
            subprocess.run(["java", "seth.ner.wrapper.SETHNERAppMut", text, useMutationFinderOnly], stdout=outfile, stderr=subprocess.PIPE, universal_newlines=True, check=True)
    except CalledProcessError as e:
        if "Error: Could not find or load main class seth.ner.wrapper.SETHNERAppMut" in e.stderr:
            raise Exception("Make sure to add seth.jar to your classpath (use repo https://github.com/juanmirocks/SETH) -- " + e.stderr)
        else:
            raise

methodName = sys.argv[1]
assert methodName in {"SETH", "MFmodified", "check_performance"}, \
    "Method name must be SETH or MFmodified or check_performance"
corpusName = sys.argv[2]
corpus = get_corpus(corpusName)
folderName = sys.argv[3]

if (methodName != 'check_performance'):
    # Given predictions folder
    folderName = os.path.join(folderName, methodName, corpusName)
    if not os.path.exists(folderName):
        os.makedirs(folderName)

    useMutationFinderOnly = "true" if methodName == "MFmodified" else "false"

    run_seth_on_corpus(corpus, folderName, useMutationFinderOnly)
else:
    BRATPartsAnnotationReader(folderName, is_predicted=True).annotate(corpus)
    ExclusiveNLDefiner().define(corpus)
    evaluation = MentionLevelEvaluator(subclass_analysis=True).evaluate(corpus)
    print(evaluation)

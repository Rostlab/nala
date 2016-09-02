import sys
import os
import subprocess
from subprocess import CalledProcessError
from nala.utils.corpora import get_corpus
from nalaf.utils.annotation_readers import BRATPartsAnnotationReader
from nalaf.learning.evaluators import MentionLevelEvaluator
from nala.preprocessing.definers import ExclusiveNLDefiner
from nalaf.utils.readers import StringReader
import requests

SERVER_PORT = 8000
SERVER_URL = 'http://localhost:'+str(SERVER_PORT)

def run_seth_on_corpus(corpus, folder, useMutationFinderOnly):
    counter = 0
    for docid, document in corpus.documents.items():
        counter += 1
        print(counter, docid)
        for partid, part in document.parts.items():
            print('\t', partid)
            run_seth_on_string(part.text, docid, partid, folder, useMutationFinderOnly)

def run_seth_on_string(text, docid, partid, folder, useMutationFinderOnly):
    filename = "{}/{}-{}.ann".format(folder, docid, partid) if folder else None
    run_seth_server_on_string_with_filename(text, filename)
    # run_seth_on_string_with_filename(text, filename, useMutationFinderOnly)

def run_set_server(useMutationFinderOnly_IGNORED):
    assert useMutationFinderOnly_IGNORED is False or useMutationFinderOnly_IGNORED == "false"
    try:
        subprocess.Popen(["java", "seth.ner.wrapper.SETHNERAppMut", "-p", str(SERVER_PORT)])
    except CalledProcessError as e:
        if "Error: Could not find or load main class seth.ner.wrapper.SETHNERAppMut" in e.stderr:
            raise Exception("Make sure to add seth.jar to your classpath (use repo https://github.com/juanmirocks/SETH) -- " + e.stderr)
        else:
            raise
    except Exception as e:
        # raise
        pass

def run_seth_server_on_string_with_filename(text, filename):
    params = {'text': text}
    r = requests.get(SERVER_URL, params=params)

    if filename:
        with open(filename, "w") as outfile:
            outfile.write(r.text)
    else:
        print(r.text)

def run_seth_on_string_with_filename(text, filename, useMutationFinderOnly):
    def run(output):
        subprocess.run(["java", "seth.ner.wrapper.SETHNERAppMut", text, useMutationFinderOnly], stdout=output, stderr=subprocess.PIPE, universal_newlines=True, check=True)

    try:
        if filename:
            with open(filename, "w") as outfile:
                run(outfile)
        else:
            run(None)

    except CalledProcessError as e:
        if "Error: Could not find or load main class seth.ner.wrapper.SETHNERAppMut" in e.stderr:
            raise Exception("Make sure to add seth.jar to your classpath (use repo https://github.com/juanmirocks/SETH) -- " + e.stderr)
        else:
            raise

methodName = sys.argv[1]
assert methodName in {"SETH", "MFmodified", "check_performance"}, \
    "Method name must be SETH or MFmodified or check_performance"
corpusName = sys.argv[2]
try:
    corpus = get_corpus(corpusName)
    folderName = sys.argv[3]
except:
    corpus = StringReader(corpusName).read()
    folderName = None  # just print out in standard output


if (methodName != 'check_performance'):
    if folderName:
        # folderName = root predictions folder
        folderName = os.path.join(folderName, methodName, corpusName)
        if not os.path.exists(folderName):
            os.makedirs(folderName)

    useMutationFinderOnly = "true" if methodName == "MFmodified" else "false"

    run_set_server(useMutationFinderOnly)

    run_seth_on_corpus(corpus, folderName, useMutationFinderOnly)
else:
    # folderName = final/leaf predictions folder
    BRATPartsAnnotationReader(folderName, is_predicted=True).annotate(corpus)
    ExclusiveNLDefiner().define(corpus)
    evaluation = MentionLevelEvaluator(subclass_analysis=True).evaluate(corpus)
    print(evaluation)

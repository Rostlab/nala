import sys
import os
import subprocess
from subprocess import CalledProcessError
from nala.utils.corpora import get_corpus

def run_seth_on_corpus(corpus, folder, useMutationFinderOnly):
    counter = 0
    for docid, document in corpus.documents.items():
        counter += 1
        print(counter, docid)
        for partid, part in document.parts.items():
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

corpusName = sys.argv[1]
corpus = get_corpus(corpusName)
folderName = sys.argv[2]
if not os.path.exists(folderName):
    os.makedirs(folderName)
useMutationFinderOnly = sys.argv[3] if len(sys.argv) > 3 else "false"

run_seth_on_corpus(corpus, folderName, useMutationFinderOnly)

from gensim.models import Word2Vec
from lxml import etree
import re
import os
import multiprocessing
from nltk import sent_tokenize

"""
Script for training word embeddings using abstracts from the whole PubMed/Medline database
"""


class MedlineSentenceGenerator:
    def __init__(self, directory):
        self.directory = directory

    @staticmethod
    def tokenize(sentence):
        sentence = re.sub('([0-9])([A-Za-z])', r'\1 \2', sentence)
        sentence = re.sub('([a-z])([A-Z])', r'\1 \2', sentence)
        sentence = re.sub('([A-Za-z])([0-9])', r'\1 \2', sentence)
        sentence = re.sub('([a-z])(fs)', r'\1 \2', sentence)
        sentence = re.sub('([\W\-_])', r' \1 ', sentence)
        return sentence.lower().split()

    def __iter__(self):
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.startswith('medline') and file.endswith('xml'):
                    try:
                        xml = os.path.join(root, file)

                        for child in etree.parse(xml).getroot():
                            for title in child.iter('ArticleTitle'):
                                yield self.tokenize(title.text)
                            for abstract in child.iter('AbstractText'):
                                for sentence in sent_tokenize(abstract.text):
                                    yield self.tokenize(sentence)
                    except:
                        pass


def train():
    medline = MedlineSentenceGenerator('/mnt/project/rost_db/medline/')

    model = Word2Vec(medline, window=10, workers=multiprocessing.cpu_count(), sg=0)
    model.save('/mnt/project/pubseq/nala/backup_we/medline_abstract_window_10_cbow_we.model')
    print(model.total_train_time, len(model.vocab))


train()

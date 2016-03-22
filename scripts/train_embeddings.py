from gensim.models import Word2Vec
from lxml import etree
import re
import os
import multiprocessing
from nltk import sent_tokenize
from spacy.en import English

"""
Script for training word embeddings using abstracts from the whole PubMed/Medline database
"""


class MedlineSentenceGenerator:
    def __init__(self, directory):
        self.directory = directory
        self.nlp = English(parser=False, entity=False)

    @staticmethod
    def tokenize(sentence):
        sentence = re.sub('([0-9])([A-Za-z])', r'\1 \2', sentence)
        sentence = re.sub('([a-z])([A-Z])', r'\1 \2', sentence)
        sentence = re.sub('([A-Za-z])([0-9])', r'\1 \2', sentence)
        sentence = re.sub('([a-z])(fs)', r'\1 \2', sentence)
        sentence = re.sub('([^\x00-\x7F])', r' \1 ', sentence)
        sentence = re.sub('([\W\-_])', r' \1 ', sentence)

        return sentence.lower().split()

    def lemmatize(self, sentence):
        spacy_doc = self.nlp.tokenizer.tokens_from_list(sentence)
        self.nlp.tagger(spacy_doc)
        return [spacy_token.lemma_ for spacy_token in spacy_doc]

    def __iter__(self):
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.startswith('medline') and file.endswith('xml'):
                    try:
                        xml = os.path.join(root, file)

                        for child in etree.parse(xml).getroot():
                            for title in child.iter('ArticleTitle'):
                                yield self.lemmatize(self.tokenize(title.text))
                            for abstract in child.iter('AbstractText'):
                                for sentence in sent_tokenize(abstract.text):
                                    yield self.lemmatize(self.tokenize(sentence))
                    except:
                        pass


def train():
    medline = MedlineSentenceGenerator('/mnt/project/rost_db/medline/')

    model = Word2Vec(medline, window=10, workers=multiprocessing.cpu_count(), sg=0)
    model.save('/mnt/project/pubseq/nala/backup_we/spacy_we.model')
    print(model.total_train_time, len(model.vocab))


train()

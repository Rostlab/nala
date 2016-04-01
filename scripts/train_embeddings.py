from gensim.models import Word2Vec
from lxml import etree
import re
import os
import multiprocessing

from nalaf.preprocessing.spliters import NLTKSplitter
from nalaf.preprocessing.tokenizers import TmVarTokenizer
from nltk import sent_tokenize
from spacy.en import English
import sys
import logging

from scripts.train_idp4 import read_data

"""
Script for training word embeddings using abstracts from the whole PubMed/Medline database
"""


class MedlineSentenceGenerator:
    def __init__(self, directory):
        self.directory = directory
        self.nlp = English(parser=False, entity=False)

    @staticmethod
    def tokenize(sentence):
        sentence = re.sub('\d', '0', sentence)

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
                                yield self.tokenize(title.text)
                            for abstract in child.iter('AbstractText'):
                                for sentence in sent_tokenize(abstract.text):
                                    yield self.tokenize(sentence)
                    except:
                        pass


class CorpusGenerator:
    """
    :type data: nalaf.structures.data.Dataset
    """
    def __init__(self):
        self.data = read_data(51, True)
        NLTKSplitter().split(self.data)
        TmVarTokenizer().tokenize(self.data)

    def __iter__(self):
        for sentence in self.data.sentences():
            yield [re.sub('\d', '0', token.word) for token in sentence]


def train():
    assert len(sys.argv) == 6
    training_folder = sys.argv[1]
    dimension = int(sys.argv[2])
    window_size = int(sys.argv[3])
    is_sg = int(sys.argv[4])
    num_iterations = int(sys.argv[5])

    use_corpus = training_folder == 'corpus'

    suffix = '{}_{}_{}_{}_{}'.format(dimension, window_size, is_sg, num_iterations, use_corpus)

    # logging.basicConfig(filename='we_{}.log'.format(suffix),
    #                     format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    logging.log(logging.INFO,
                'start training a model {}'.format(suffix))

    if use_corpus:
        dataset = CorpusGenerator()
    else:
        dataset = MedlineSentenceGenerator(training_folder)

    model = Word2Vec(dataset, window=window_size, workers=multiprocessing.cpu_count(), sg=is_sg, size=dimension,
                     iter=num_iterations)

    model.init_sims(True)
    model.save('/mnt/project/pubseq/nala/backup_we/number_replaced_{}.model'.format(suffix))

    print(model.total_train_time, len(model.vocab))


train()
# run with
# echo "python nala/scripts/train_embeddings.py /mnt/project/rost_db/medline/ 100 15"|at -m NOW

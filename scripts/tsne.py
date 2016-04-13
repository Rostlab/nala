import os
import re

import numpy as np
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from nalaf.features.embeddings import DiscreteWordEmbeddingsFeatureGenerator
from sklearn.manifold import TSNE
from scripts.train_idp4 import read_data
from nalaf.preprocessing.spliters import NLTKSplitter
from nalaf.preprocessing.tokenizers import TmVarTokenizer


def transform(model_name, ax):
    m = Word2Vec.load(model_name)

    words = [w for w in get_words() if w in m]
    # words = [w for w in m.vocab]

    labels = get_word_labels(words)

    data = np.vstack(m[w] for i, w in enumerate(words))

    del m

    model = TSNE(n_components=2, random_state=0, verbose=True)

    y = model.fit_transform(data)

    ax.scatter(y[:, 0], y[:, 1], c=labels)
    ax.set_title(model_name.split('/')[-1])


def get_words():
    return set(re.sub('\d', '0', token.word.lower()) for token in data.tokens())


def get_word_labels(words):
    for part in data.parts():
        part.percolate_tokens_to_entities()
    ann_words = set(re.sub('\d', '0', token.word.lower()) for ann in data.annotations() for token in ann.tokens)

    return ['r' if word in ann_words else 'b' for word in words]


data = read_data(51, True)
NLTKSplitter().split(data)
TmVarTokenizer().tokenize(data)

transform('/home/abojchevski/projects/nala/nala/data/models/300_10_0_5_False.model', plt.gca())
plt.show()


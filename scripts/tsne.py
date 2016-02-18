import numpy as np
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
from scripts.train_idp4 import read_data
from nalaf.preprocessing.spliters import NLTKSplitter
from nalaf.preprocessing.tokenizers import TmVarTokenizer


def transform():
    m = Word2Vec.load('../nala/data/word_embeddings/word_embeddings.model')

    words = [w for w in get_words() if w in m]

    labels = get_word_labels(words)

    data = np.vstack(m[w] for i, w in enumerate(words))

    del m

    model = TSNE(n_components=2, random_state=0, verbose=True)

    y = model.fit_transform(data)

    plt.rcParams['image.cmap'] = 'brg'
    plt.scatter(y[:, 0], y[:, 1], c=labels)
    plt.show()


def get_words():
    return set(t.word.lower() for t in data.tokens())


def get_word_labels(words):
    for part in data.parts():
        part.percolate_tokens_to_entities()
    ann_words = set(token.word.lower() for ann in data.annotations() for token in ann.tokens)

    return ['r' if word in ann_words else 'b' for word in words]

data = read_data(41)
NLTKSplitter().split(data)
TmVarTokenizer().tokenize(data)
transform()

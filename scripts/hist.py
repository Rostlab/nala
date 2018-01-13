from gensim.models import Word2Vec
import numpy as np
import matplotlib.pyplot as plt
from nalaf.preprocessing.spliters import NLTKSplitter
from nalaf.preprocessing.tokenizers import TmVarTokenizer

from scripts.train_idp4 import read_data

data = read_data(51)
NLTKSplitter().split(data)
TmVarTokenizer().tokenize(data)
words = set(token.word for token in data.tokens())

m = Word2Vec.load('/home/abojchevski/projects/nala/nala/data/word_embeddings_2016-03-28/word_embeddings.model')
data = np.vstack(m[w] for w in m.vocab if w in words)
data1 = np.vstack(m[w] for w in m.vocab if w not in words)
print(data.shape)
plt.hist(data, bins=100, alpha=0.5)
plt.hist(data1, bins=100, alpha=0.5)
#
# fx, ax = plt.subplots(10, 10, sharex=True, sharey=True)
# ax = ax.ravel()
#
# for i in range(len(ax)):
#     ax[i].hist(data[:, i], bins=100, alpha=0.5)
#     ax[i].hist(data1[:, i], bins=100, alpha=0.5)
plt.show()
from nala.utils.corpora import get_corpus
from nalaf.preprocessing.spliters import NLTKSplitter
from nalaf.preprocessing.tokenizers import TmVarTokenizer

data = get_corpus('nala_training_1')

NLTKSplitter().split(data)
TmVarTokenizer().tokenize(data)
from nalaf.features.embeddings import BinarizedWordEmbeddingsFeatureGenerator

BinarizedWordEmbeddingsFeatureGenerator('/home/abojchevski/projects/nala/nala/data/word_embeddings_2016-03-28/word_embeddings.model').generate(data)

for token in data.tokens():
    print(token.features, token.end)

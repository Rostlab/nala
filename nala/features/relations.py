from nala.features import FeatureGenerator
from nltk.stem import PorterStemmer
from math import log2
from operator import itemgetter

class NamedEntityCountFeatureGenerator(FeatureGenerator):
    """
    Generates Named Entity Count for each sentence that contains an edge

    :type entity_type: str
    :type mode: str
    :type feature_set: dict
    :type training_mode: bool
    """
    def __init__(self, entity_type, feature_set, training_mode=True):
        self.entity_type = entity_type
        """type of entity"""
        self.training_mode = training_mode
        """whether the mode is training or testing"""
        self.feature_set = feature_set
        """the feature set"""

    def generate(self, dataset):
        for edge in dataset.edges():
            entities = edge.part.get_entities_in_sentence(edge.sentence_id, self.entity_type)
            feature_name = self.entity_type + '_count_[' + str(len(entities)) + ']'
            if self.training_mode:
                if feature_name not in self.feature_set:
                    self.feature_set[feature_name] = len(self.feature_set.keys())+1
                edge.features[self.feature_set[feature_name]] = 1
            else:
                if feature_name in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name]] = 1

class BagOfWordsFeatureGenerator(FeatureGenerator):
    """
    Generates Bag of Words representation for each sentence that contains an edge

    :type feature_set: nala.structures.data.FeatureDictionary
    :type training_mode: bool
    """
    def __init__(self, feature_set, training_mode=True):
        self.feature_set = feature_set
        """the feature set for the dataset"""
        self.training_mode = training_mode
        """whether the mode is training or testing"""

    def generate(self, dataset):
        self.stop_words = []
        with open('/home/ashish/projects/thesis-alex-carsten/nala/features/stopwords.txt') as f:
            for line in f:
                self.stop_words.append(line.strip())
        for edge in dataset.edges():
            sentence = edge.part.sentences[edge.sentence_id]
            if self.training_mode:
                for token in sentence:
                    if token.word not in self.stop_words:
                        feature_name = 'bow_' + token.word + '_[0]'
                        if feature_name not in self.feature_set:
                            self.feature_set[feature_name] = len(self.feature_set.keys())+1
                        edge.features[self.feature_set[feature_name]] = 1
            else:
                for token in sentence:
                    feature_name = 'bow_' + token.word + '_[0]'
                    if feature_name in self.feature_set.keys():
                        edge.features[self.feature_set[feature_name]] = 1

class StemmedBagOfWordsFeatureGenerator(FeatureGenerator):
    """
    Generates stemmed Bag of Words representation for each sentence that contains
    an edge, using the function given in the argument.

    By default it uses Porter stemmer

    :type feature_set: nala.structures.data.FeatureDictionary
    :type training_mode: bool
    """

    def __init__(self, feature_set, training_mode=True):
        self.feature_set = feature_set
        """the feature set for the dataset"""
        self.training_mode = training_mode
        """whether the mode is training or testing"""
        self.stemmer = PorterStemmer()
        """an instance of the PorterStemmer"""
        self.stop_words = None

    def generate(self, dataset):
        self.stop_words = []
        with open('/home/ashish/projects/thesis-alex-carsten/nala/features/stopwords.txt') as f:
            for line in f:
                self.stop_words.append(line.strip())
        for edge in dataset.edges():
            sentence = edge.part.sentences[edge.sentence_id]
            if self.training_mode:
                for token in sentence:
                    if self.stemmer.stem(token.word) not in self.stop_words:
                        feature_name = 'bow_stem_' + self.stemmer.stem(token.word) + '_[0]'
                        if feature_name not in self.feature_set:
                            self.feature_set[feature_name] = len(self.feature_set.keys())+1
                        edge.features[self.feature_set[feature_name]] = 1
            else:
                for token in sentence:
                    feature_name = 'bow_stem_' + self.stemmer.stem(token.word) + '_[0]'
                    if feature_name in self.feature_set.keys():
                        edge.features[self.feature_set[feature_name]] = 1

class OrderOfEntitiesFeatureGenerator(FeatureGenerator):
    """
    Generates the order in which the entities are present in the sentence.
    That is, whether it is '...entity1...entity2...' or '...entity2...entity1...'

    Value of 1 means that the order is '...entity1...entity2...'
    Value of 0 means that the order is '...entity2...entity1...'

    :type feature_set: nala.structures.data.FeatureDictionary
    :type training_mode: bool
    """
    def __init__(self, feature_set, training_mode=True):
        self.feature_set = feature_set
        """the feature set for the dataset"""
        self.training_mode = training_mode
        """whether the mode is training or testing"""

    def generate(self, dataset):
        for edge in dataset.edges():
            feature_name = 'order_entities_[0]'
            if self.training_mode:
                if feature_name not in self.feature_set.keys():
                    self.feature_set[feature_name] = len(self.feature_set.keys())+1
                if edge.entity1.offset < edge.entity2.offset:
                    edge.features[self.feature_set[feature_name]] = 1
            else:
                if feature_name in self.feature_set.keys():
                    if edge.entity1.offset < edge.entity2.offset:
                        edge.features[self.feature_set[feature_name]] = 1


class CapitalizedTokenFeatureGenerator(FeatureGenerator):
    """
    Checks if the entity in the edge is capitalized or not.

    Value of 1 means that the entity is capitalized
    Value of 0 means that the entity is not capitalized

    :type feature_set: nala.structures.data.FeatureDictionary
    :type training_mode: bool
    """
    def __init__(self, feature_set, training_mode=True):
        self.feature_set = feature_set
        """the feature set for the dataset"""
        self.training_mode = training_mode
        """whether the mode is training or testing"""

    def generate(self, dataset):
        feature_name_1 = 'entity_1_capitalized_[0]'
        feature_name_2 = 'entity_2_capitalized_[0]'
        if self.training_mode:
            if feature_name_1 not in self.feature_set.keys():
                self.feature_set[feature_name_1] = len(self.feature_set.keys()) + 1
            if feature_name_2 not in self.feature_set.keys():
                self.feature_set[feature_name_2] = len(self.feature_set.keys()) + 1
            for edge in dataset.edges():
                if edge.entity1.text.isupper():
                    edge.features[self.feature_set[feature_name_1]] = 1
                if edge.entity2.text.isupper():
                    edge.features[self.feature_set[feature_name_2]] = 1
        else:
            for edge in dataset.edges():
                if feature_name_1 in self.feature_set.keys():
                    if edge.entity1.text.isupper():
                        edge.features[self.feature_set[feature_name_1]] = 1
                if feature_name_2 in self.feature_set.keys():
                    if edge.entity2.text.isupper():
                        edge.features[self.feature_set[feature_name_2]] = 1


class WordFilterFeatureGenerator(FeatureGenerator):
    """
    Checks if the sentence containing an edge contains any of the words
    given in the list.

    Value of 1 means that the sentence contains that word
    Value of 0 means that the sentence does not contain the word

    :type feature_set: nala.structures.data.FeatureDictionary
    :type words: list[str]
    :type stem: bool
    :type training_mode: bool
    """
    def __init__(self, feature_set, words, stem=True, training_mode=True):
        self.feature_set = feature_set
        """the feature set for the dataset"""
        self.words = words
        """a list of words to check for their presence in the sentence"""
        self.stem = stem
        """whether the words in the sentence and the list should be stemmed"""
        self.training_mode = True
        """whether the mode is training or testing"""
        self.stemmer = PorterStemmer()

    def generate(self, dataset):
        if self.stem:
            stemmed_words = [ self.stemmer.stem(word) for word in self.words ]
            if self.training_mode:
                for edge in dataset.edges():
                    sentence = edge.part.sentences[edge.sentence_id]
                    for token in sentence:
                        if self.stemmer.stem(token.word) in stemmed_words:
                            feature_name = 'word_filter_stem_' + self.stemmer.stem(token.word) + '_[0]'
                            if feature_name not in self.feature_set.keys():
                                self.feature_set[feature_name] = len(self.feature_set.keys()) + 1
                            edge.features[self.feature_set[feature_name]] = 1
            else:
                for edge in dataset.edges():
                    sentence = edge.part.sentences[edge.sentence_id]
                    for token in sentence:
                        if self.stemmer.stem(token.word) in stemmed_words:
                            feature_name = 'word_filter_stem_' + self.stemmer.stem(token.word) + '_[0]'
                            if feature_name in self.feature_set.keys():
                                edge.features[self.feature_set[feature_name]] = 1
        else:
            if self.training_mode:
                for edge in dataset.edges():
                    sentence = edge.part.sentences[edge.sentence_id]
                    for token in sentence:
                        if token.word in self.words:
                            feature_name = 'word_filter_' + token.word + '_[0]'
                            if feature_name not in self.feature_set.keys():
                                self.feature_set[feature_name] = len(self.feature_set.keys()) + 1
                            edge.features[self.feature_set[feature_name]] = 1
            else:
                for edge in dataset.edges():
                    sentence = edge.part.sentences[edge.sentence_id]
                    for token in sentence:
                        if token in self.words:
                            feature_name = 'word_filter_' + token.word + '_[0]'
                            if feature_name in self.feature_set.keys():
                                edge.features[self.feature_set[feature_name]] = 1


class NPChunkRootFeatureGenerator(FeatureGenerator):
    """
    Generate Noun Phrase Chunks for each sentence containing an edge and store
    the roots of each noun phrase chunk

    This requires the Python module SpaCy (http://spacy.io/) and NumPy. SpaCy
    can be installed by `pip3 install spacy`. Additionally it also requires
    the package data, which can be downloaded using
    `python3 -m spacy.en.download all`

    :type feature_set: nala.structures.data.FeatureDictionary
    :type nlp: spacy.en.English
    :type training_mode: bool
    """
    def __init__(self, feature_set, nlp, training_mode=True):
        self.feature_set = feature_set
        """the feature set for the dataset"""
        self.nlp = nlp
        """an instance of spacy.en.English"""
        self.training_mode = training_mode
        """whether the mode is training or testing"""

    def generate(self, dataset):
        if self.training_mode:
            for edge in dataset.edges():
                sent = edge.part.get_sentence_string_array()[edge.sentence_id]
                sentence = self.nlp(sent, parse=True, tag=True)
                for chunk in sentence.noun_chunks:
                    feature_name = 'np_chunk_root_' + chunk.root.orth_ + '_[0]'
                    if feature_name not in self.feature_set.keys():
                        self.feature_set[feature_name] = len(self.feature_set.keys()) + 1
                    edge.features[self.feature_set[feature_name]] = 1
        else:
            for edge in dataset.edges():
                sent = edge.part.get_sentence_string_array()[edge.sentence_id]
                sentence = self.nlp(sent, parse=True, tag=True)
                for chunk in sentence.noun_chunks:
                    feature_name = 'np_chunk_root_' + chunk.root.orth_ + '_[0]'
                    if feature_name in self.feature_set.keys():
                        edge.features[self.feature_set[feature_name]] = 1


class EntityHeadTokenFeatureGenerator(FeatureGenerator):
    """
    Generate the head token for each of the entities and generate features based
    on those. The following features are generated:
    * Entity Head Token Text
    * Entity Head Token POS
    * Entity Head Token Lemma
    * Entity Head Token Shape
    * Entity Head Token Vector Normalization
    * Entity Head Token Normalization
    * Entity Head Token Prefix
    * Entity Head Token Suffix
    * Entity Head Token Lex ID
    * Tokens left of the Entity Head Token
    * Tokens right of the Entity Head Token
    * Entity Head Token Tag
    * Entity Head Token Stemmed Part
    * Entity Head Token Non-stemmed Part

    :type feature_set: nala.structures.data.FeatureDictionary
    :type nlp: spacy.en.English
    :type training_mode: bool
    """
    def __init__(self, feature_set, nlp, training_mode=True):
        self.feature_set = feature_set
        """the feature set for the dataset"""
        self.nlp = nlp
        """an instance of spacy.en.English"""
        self.training_mode = training_mode
        """whether the mode is training or testing"""
        self.stemmer = PorterStemmer()
        """an instance of PorterStemmer"""

    def generate(self, dataset):
        if self.training_mode:
            for edge in dataset.edges():
                ent1 = self.nlp(edge.entity1.text)
                ent1_root = next(ent1.sents).root
                while (ent1_root != ent1_root.head):
                    ent1_root = ent1_root.head
                ent2 = self.nlp(edge.entity2.text)
                ent2_root = next(ent2.sents).root
                while (ent2_root != ent2_root.head):
                    ent2_root = ent2_root.head
                feature_name_1_1 = 'entity_1_root_token_text_' + ent1_root.text + '_[0]'
                feature_name_1_2 = 'entity_1_root_token_pos_' + ent1_root.pos_ + '_[0]'
                feature_name_1_3 = 'entity_1_root_token_lemma_' + ent1_root.lemma_ + '_[0]'
                feature_name_1_4 = 'entity_1_root_token_tag_' + ent1_root.tag_ + '_[0]'
                feature_name_1_5 = 'entity_1_root_token_shape_' + ent1_root.shape_ + '_[0]'
                feature_name_1_6 = 'entity_1_root_token_norm_' + ent1_root.norm_ + '_[0]'
                feature_name_1_7 = 'entity_1_root_token_vector_norm_[0]'
                feature_name_1_8 = 'entity_1_root_token_lex_id_[0]'
                feature_name_1_9 = 'entity_1_root_token_n_lefts_[' + str(ent1_root.n_lefts) + ']'
                feature_name_1_10 = 'entity_1_root_token_n_rights_[' + str(ent1_root.n_rights) + ']'
                feature_name_1_11 = 'entity_1_root_token_prefix_' + ent1_root.prefix_ + '_[0]'
                feature_name_1_12 = 'entity_1_root_token_suffix_' + ent1_root.suffix_ + '_[0]'
                ent1_stem = self.stemmer.stem(ent1_root.text)
                ent1_non_stem = ent1_root.text[len(ent1_stem):]
                feature_name_1_13 = 'entity_1_root_token_stem_' + ent1_stem + '_[0]'
                feature_name_1_14 = 'entity_1_root_token_non_stem_' + ent1_non_stem + '_[0]'
                feature_name_2_1 = 'entity_2_root_token_text_' + ent2_root.text + '_[0]'
                feature_name_2_2 = 'entity_2_root_token_pos_' + ent2_root.pos_ + '_[0]'
                feature_name_2_3 = 'entity_2_root_token_lemma_' + ent2_root.lemma_ + '_[0]'
                feature_name_2_4 = 'entity_2_root_token_tag_' + ent2_root.tag_ + '_[0]'
                feature_name_2_5 = 'entity_2_root_token_shape_' + ent2_root.shape_ + '_[0]'
                feature_name_2_6 = 'entity_2_root_token_norm_' + ent2_root.norm_ + '_[0]'
                feature_name_2_7 = 'entity_2_root_token_vector_norm_[0]'
                feature_name_2_8 = 'entity_2_root_token_lex_id_[0]'
                feature_name_2_9 = 'entity_2_root_token_n_lefts_[' + str(ent2_root.n_lefts) + ']'
                feature_name_2_10 = 'entity_2_root_token_n_rights_[' + str(ent2_root.n_rights) + ']'
                feature_name_2_11 = 'entity_2_root_token_prefix_' + ent2_root.prefix_ + '_[0]'
                feature_name_2_12 = 'entity_2_root_token_suffix_' + ent2_root.suffix_ + '_[0]'
                ent2_stem = self.stemmer.stem(ent2_root.text)
                ent2_non_stem = ent2_root.text[len(ent2_stem):]
                feature_name_2_13 = 'entity_1_root_token_stem_' + ent2_stem + '_[0]'
                feature_name_2_14 = 'entity_1_root_token_non_stem_' + ent2_non_stem + '_[0]'

                if feature_name_1_1 not in self.feature_set.keys():
                    self.feature_set[feature_name_1_1] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_1_1]] = 1

                if feature_name_1_2 not in self.feature_set.keys():
                    self.feature_set[feature_name_1_2] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_1_2]] = 1

                if feature_name_1_3 not in self.feature_set.keys():
                    self.feature_set[feature_name_1_3] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_1_3]] = 1

                if feature_name_1_4 not in self.feature_set.keys():
                    self.feature_set[feature_name_1_4] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_1_4]] = 1

                if feature_name_1_5 not in self.feature_set.keys():
                    self.feature_set[feature_name_1_5] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_1_5]] = 1

                if feature_name_1_6 not in self.feature_set.keys():
                    self.feature_set[feature_name_1_6] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_1_6]] = 1

                if feature_name_1_7 not in self.feature_set.keys():
                    self.feature_set[feature_name_1_7] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_1_7]] = ent1_root.vector_norm

                if feature_name_1_8 not in self.feature_set.keys():
                    self.feature_set[feature_name_1_8] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_1_8]] = ent1_root.lex_id

                if feature_name_1_9 not in self.feature_set.keys():
                    self.feature_set[feature_name_1_9] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_1_9]] = 1

                if feature_name_1_10 not in self.feature_set.keys():
                    self.feature_set[feature_name_1_10] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_1_10]] = 1

                if feature_name_1_11 not in self.feature_set.keys():
                    self.feature_set[feature_name_1_11] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_1_11]] = 1

                if feature_name_1_12 not in self.feature_set.keys():
                    self.feature_set[feature_name_1_12] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_1_12]] = 1

                if feature_name_1_13 not in self.feature_set.keys():
                    self.feature_set[feature_name_1_13] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_1_13]] = 1

                if feature_name_1_14 not in self.feature_set.keys():
                    self.feature_set[feature_name_1_14] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_1_14]] = 1

                if feature_name_2_1 not in self.feature_set.keys():
                    self.feature_set[feature_name_2_1] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_2_1]] = 1

                if feature_name_2_2 not in self.feature_set.keys():
                    self.feature_set[feature_name_2_2] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_2_2]] = 1

                if feature_name_2_3 not in self.feature_set.keys():
                    self.feature_set[feature_name_2_3] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_2_3]] = 1

                if feature_name_2_4 not in self.feature_set.keys():
                    self.feature_set[feature_name_2_4] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_2_4]] = 1

                if feature_name_2_5 not in self.feature_set.keys():
                    self.feature_set[feature_name_2_5] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_2_5]] = 1

                if feature_name_2_6 not in self.feature_set.keys():
                    self.feature_set[feature_name_2_6] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_2_6]] = 1

                if feature_name_2_7 not in self.feature_set.keys():
                    self.feature_set[feature_name_2_7] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_2_7]] = ent2_root.vector_norm

                if feature_name_2_8 not in self.feature_set.keys():
                    self.feature_set[feature_name_2_8] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_2_8]] = ent2_root.lex_id

                if feature_name_2_9 not in self.feature_set.keys():
                    self.feature_set[feature_name_2_9] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_2_9]] = 1

                if feature_name_2_10 not in self.feature_set.keys():
                    self.feature_set[feature_name_2_10] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_2_10]] = 1

                if feature_name_2_11 not in self.feature_set.keys():
                    self.feature_set[feature_name_2_11] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_2_11]] = 1

                if feature_name_2_12 not in self.feature_set.keys():
                    self.feature_set[feature_name_2_12] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_2_12]] = 1

                if feature_name_2_13 not in self.feature_set.keys():
                    self.feature_set[feature_name_2_13] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_2_13]] = 1

                if feature_name_2_14 not in self.feature_set.keys():
                    self.feature_set[feature_name_2_14] = len(self.feature_set.keys()) + 1
                edge.features[self.feature_set[feature_name_2_14]] = 1
        else:
            for edge in dataset.edges():
                ent1 = self.nlp(edge.entity1.text)
                ent1_root = next(ent1.sents).root
                while (ent1_root != ent1_root.head):
                    ent1_root = ent1_root.head
                ent2 = self.nlp(edge.entity2.text)
                ent2_root = next(ent2.sents).root
                while (ent2_root != ent2_root.head):
                    ent2_root = ent2_root.head
                feature_name_1_1 = 'entity_1_root_token_text_' + ent1_root.text + '_[0]'
                feature_name_1_2 = 'entity_1_root_token_pos_' + ent1_root.pos_ + '_[0]'
                feature_name_1_3 = 'entity_1_root_token_lemma_' + ent1_root.lemma_ + '_[0]'
                feature_name_1_4 = 'entity_1_root_token_tag_' + ent1_root.tag_ + '_[0]'
                feature_name_1_5 = 'entity_1_root_token_shape_' + ent1_root.shape_ + '_[0]'
                feature_name_1_6 = 'entity_1_root_token_norm_' + ent1_root.norm_ + '_[0]'
                feature_name_1_7 = 'entity_1_root_token_vector_norm_[0]'
                feature_name_1_8 = 'entity_1_root_token_lex_id_[0]'
                feature_name_1_9 = 'entity_1_root_token_n_lefts_[' + str(ent1_root.n_lefts) + ']'
                feature_name_1_10 = 'entity_1_root_token_n_rights_[' + str(ent1_root.n_rights) + ']'
                feature_name_1_11 = 'entity_1_root_token_prefix_' + ent1_root.prefix_ + '_[0]'
                feature_name_1_12 = 'entity_1_root_token_suffix_' + ent1_root.suffix_ + '_[0]'
                ent1_stem = self.stemmer.stem(ent1_root.text)
                ent1_non_stem = ent1_root.text[len(ent1_stem):]
                feature_name_1_13 = 'entity_1_root_token_stem_' + ent1_stem + '_[0]'
                feature_name_1_14 = 'entity_1_root_token_non_stem_' + ent1_non_stem + '_[0]'
                feature_name_2_1 = 'entity_2_root_token_text_' + ent2_root.text + '_[0]'
                feature_name_2_2 = 'entity_2_root_token_pos_' + ent2_root.pos_ + '_[0]'
                feature_name_2_3 = 'entity_2_root_token_lemma_' + ent2_root.lemma_ + '_[0]'
                feature_name_2_4 = 'entity_2_root_token_tag_' + ent2_root.tag_ + '_[0]'
                feature_name_2_5 = 'entity_2_root_token_shape_' + ent2_root.shape_ + '_[0]'
                feature_name_2_6 = 'entity_2_root_token_norm_' + ent2_root.norm_ + '_[0]'
                feature_name_2_7 = 'entity_2_root_token_vector_norm_[0]'
                feature_name_2_8 = 'entity_2_root_token_lex_id_[0]'
                feature_name_2_9 = 'entity_2_root_token_n_lefts_[' + str(ent2_root.n_lefts) + ']'
                feature_name_2_10 = 'entity_2_root_token_n_rights_[' + str(ent2_root.n_rights) + ']'
                feature_name_2_11 = 'entity_2_root_token_prefix_' + ent2_root.prefix_ + '_[0]'
                feature_name_2_12 = 'entity_2_root_token_suffix_' + ent2_root.suffix_ + '_[0]'
                ent2_stem = self.stemmer.stem(ent2_root.text)
                ent2_non_stem = ent2_root.text[len(ent2_stem):]
                feature_name_2_13 = 'entity_1_root_token_stem_' + ent2_stem + '_[0]'
                feature_name_2_14 = 'entity_1_root_token_non_stem_' + ent2_non_stem + '_[0]'

                if feature_name_1_1 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_1_1]] = 1
                if feature_name_1_2 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_1_2]] = 1
                if feature_name_1_3 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_1_3]] = 1
                if feature_name_1_4 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_1_4]] = 1
                if feature_name_1_5 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_1_5]] = 1
                if feature_name_1_6 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_1_6]] = 1
                if feature_name_1_7 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_1_7]] = ent1_root.vector_norm
                if feature_name_1_8 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_1_8]] = ent1_root.lex_id
                if feature_name_1_9 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_1_9]] = 1
                if feature_name_1_10 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_1_10]] = 1
                if feature_name_1_11 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_1_11]] = 1
                if feature_name_1_12 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_1_12]] = 1
                if feature_name_1_13 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_1_13]] = 1
                if feature_name_1_14 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_1_14]] = 1

                if feature_name_2_1 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_2_1]] = 1
                if feature_name_2_2 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_2_2]] = 1
                if feature_name_2_3 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_2_3]] = 1
                if feature_name_2_4 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_2_4]] = 1
                if feature_name_2_5 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_2_5]] = 1
                if feature_name_2_6 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_2_6]] = 1
                if feature_name_2_7 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_2_7]] = ent2_root.vector_norm
                if feature_name_2_8 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_2_8]] = ent2_root.lex_id
                if feature_name_2_9 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_2_9]] = 1
                if feature_name_2_10 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_2_10]] = 1
                if feature_name_2_11 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_2_11]] = 1
                if feature_name_2_12 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_2_12]] = 1
                if feature_name_2_13 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_2_13]] = 1
                if feature_name_2_14 in self.feature_set.keys():
                    edge.features[self.feature_set[feature_name_2_14]] = 1


class DependencyChainFeatureGenerator(FeatureGenerator):
    """
    Generate the dependency chain for each token in the sentence containing an
    edge

    :type feature_set: nala.structures.data.FeatureDictionary
    :type nlp: spacy.en.English
    :type training_mode: bool
    """
    def __init__(self, feature_set, nlp, training_mode=True):
        self.feature_set = feature_set
        """Feature set for the dataset"""
        self.nlp = nlp
        """an instance of spacy.en.English"""
        self.training_mode = training_mode
        """whether the mode is training or testing"""

    def generate(self, dataset):
        for edge in dataset.edges():
            sent = edge.part.get_sentence_string_array()[edge.sentence_id]
            parsed = self.nlp(sent)
            sentence = next(sent.sents)
            dependencies = {}
            for token in sentence:
                token_dependency = self.dependency_labels_to_root(token)
                feature_name_1 = 'dep_chain_len_[' + len(token_dependency) +']'
                if self.training_mode:
                    if feature_name_1 not in self.feature_set.keys():
                        self.feature_set[feature_name_1] = len(self.feature_set.keys())
                        edge.features[self.feature_set[feature_name_1]] = 0
                    edge.features[self.feature_set[feature_name_1]] += 1
                else:
                    if feature_name_1 in self.feature_set.keys():
                        if self.feature_set[feature_name_1] not in edge.features.keys():
                            edge.features[self.feature_set[feature_name_1]] = 0
                        edge.features[self.feature_set[feature_name_1]] += 1


    def dependency_labels_to_root(self, token):
        """Walk up the syntactic tree, collecting the arc labels."""
        dep_labels = []
        token = token.head
        while token.head is not token:
            dep_labels.append((token.orth_, token.dep_))
            token = token.head
        return dep_labels


def calculateInformationGain(feature_set, dataset, output_file):
    number_pos_instances = 0
    number_neg_instances = 0

    for edge in dataset.edges():
        if edge.target == 1:
            number_pos_instances += 1
        else:
            number_neg_instances += 1

    number_total_instances = number_pos_instances + number_neg_instances
    percentage_pos_instances = number_pos_instances / number_total_instances
    percentage_neg_instances = number_neg_instances / number_total_instances

    first_ent_component = -1 * (percentage_pos_instances * log2(percentage_pos_instances) + percentage_neg_instances * log2(percentage_neg_instances))
    feature_list = []
    for key, value in feature_set.items():
        feature_present_in_pos = 0
        feature_present_in_neg = 0
        feature_absent_in_pos = 0
        feature_absent_in_neg = 0
        total_feature_present = 0
        total_feature_absent = 0

        for edge in dataset.edges():
            if edge.target == 1:
                if value in edge.features.keys():
                    feature_present_in_pos += 1
                    total_feature_present += 1
                else:
                    feature_absent_in_pos += 1
                    total_feature_absent +=1
            if edge.target == -1:
                if value in edge.features.keys():
                    feature_present_in_neg += 1
                    total_feature_present += 1
                else:
                    feature_absent_in_neg += 1
                    total_feature_absent += 1

        percentage_pos_given_feature = 0
        percentage_neg_given_feature = 0
        if (total_feature_present > 0):
            percentage_pos_given_feature = feature_present_in_pos / total_feature_present
            percentage_neg_given_feature = feature_present_in_neg / total_feature_present

        percentage_pos_given_feature_log = 0
        percentage_neg_given_feature_log = 0
        if percentage_pos_given_feature > 0:
            percentage_pos_given_feature_log = log2(percentage_pos_given_feature)
        if percentage_neg_given_feature > 0:
            percentage_neg_given_feature_log = log2(percentage_neg_given_feature)

        second_emp_component_factor = percentage_pos_given_feature * percentage_pos_given_feature_log + \
                            percentage_neg_given_feature * percentage_neg_given_feature_log

        percentage_feature_given_pos = feature_present_in_pos / number_pos_instances
        percentage_feature_given_neg = feature_present_in_pos / number_neg_instances
        percentage_feature = percentage_feature_given_pos * percentage_pos_instances + \
                    percentage_feature_given_neg * percentage_neg_instances

        second_ent_component = percentage_feature * second_emp_component_factor
        percentage_pos_given_feature_component = 0
        percentage_neg_given_feature_component = 0
        if total_feature_absent>0:
            percentage_pos_given_feature_component = feature_absent_in_pos / total_feature_absent
            percentage_neg_given_feature_component = feature_absent_in_neg / total_feature_absent

        percentage_pos_given_feature_component_log = 0
        percentage_neg_given_feature_component_log = 0
        if percentage_pos_given_feature_component>0:
            percentage_pos_given_feature_component_log = log2(percentage_pos_given_feature_component)
        if percentage_neg_given_feature_component>0:
            percentage_neg_given_feature_component_log = log2(percentage_neg_given_feature_component)

        third_component_multi_factor = percentage_pos_given_feature_component * percentage_pos_given_feature_component_log + \
                percentage_neg_given_feature_component * percentage_neg_given_feature_component_log

        percentage_feature_comp_given_pos = feature_absent_in_pos / number_pos_instances
        percentage_feature_comp_given_neg = feature_absent_in_neg / number_neg_instances
        percentage_feature_comp = percentage_feature_comp_given_pos * percentage_pos_instances + \
                    percentage_feature_comp_given_neg * percentage_neg_instances

        third_ent_component = percentage_feature_comp * third_component_multi_factor
        entropy = first_ent_component + second_ent_component + third_ent_component

        feature_list.append([key, value, entropy])

    feature_list = sorted(feature_list, key=itemgetter(2), reverse=True)

    with open(output_file, 'w') as f:
        for array in feature_list:
            key, value, entropy = array[0], array[1], array[2]
            f.write(str(key)+':'+str(value)+':'+str(entropy)+'\n')
    f.close()

    return feature_list

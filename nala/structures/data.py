from collections import OrderedDict
from nala.utils import MUT_CLASS_ID
import math
import re
from nala.utils.qmath import arithmetic_mean
from nala.utils.qmath import harmonic_mean


class Dataset:
    """
    Class representing a group of documents.
    Instances of this class are the main object that gets passed around and modified by different modules.

    :type documents: dict
    """

    def __init__(self):
        self.documents = OrderedDict()
        """
        documents the dataset consists of, encoded as a dictionary
        where the key (string) is the id of the document, for example PubMed id
        and the value is an instance of Document
        """

    def __len__(self):
        """
        the length (size) of a dataset equals to the number of documents it has
        """
        return len(self.documents)

    def __iter__(self):
        """
        when iterating through the dataset iterate through each document
        """
        for doc_id, document in self.documents.items():
            yield document

    def __contains__(self, item):
        return item in self.documents

    def parts(self):
        """
        helper functions that iterates through all parts
        that is each part of each document in the dataset

        :rtype: collections.Iterable[Part]
        """
        for document in self:
            for part in document:
                yield part

    def annotations(self):
        """
        helper functions that iterates through all parts
        that is each part of each document in the dataset

        :rtype: collections.Iterable[Annotation]
        """
        for part in self.parts():
            for annotation in part.annotations:
                yield annotation

    def predicted_annotations(self):
        """
        helper functions that iterates through all parts
        that is each part of each document in the dataset

        :rtype: collections.Iterable[Annotation]
        """
        for part in self.parts():
            for annotation in part.predicted_annotations:
                yield annotation

    def sentences(self):
        """
        helper functions that iterates through all sentences
        that is each sentence of each part of each document in the dataset

        :rtype: collections.Iterable[list[Token]]
        """
        for part in self.parts():
            for sentence in part.sentences:
                yield sentence

    def tokens(self):
        """
        helper functions that iterates through all tokens
        that is each token of each sentence of each part of each document in the dataset

        :rtype: collections.Iterable[Token]
        """
        for sentence in self.sentences():
            for token in sentence:
                yield token

    def partids_with_parts(self):
        """
        helper function that yields part id with part

        :rtype: collections.Iterable[(str, Part)]
        """
        for document in self:
            for part_id, part in document.key_value_parts():
                yield part_id, part

    def annotations_with_partids(self):
        """
        helper function that return annotation object with part id
        to be able to find out abstract or full document

        :rtype: collections.Iterable[(str, Annotation)]
        """
        for part_id, part in self.partids_with_parts():
            for annotation in part.annotations:
                yield part_id, annotation

    def all_annotations_with_ids(self):
        """
        yields pubmedid, partid and ann through whole dataset

        :rtype: collections.Iterable[(str, str, Annotation)]
        """
        for pubmedid, doc in self.documents.items():
            for partid, part in doc.key_value_parts():
                for ann in part.annotations:
                    yield pubmedid, partid, ann

    def form_predicted_annotations(self, class_id, aggregator_function=arithmetic_mean):
        """
        Populates part.predicted_annotations with a list of Annotation objects
        based on the values of the field predicted_label for each token.

        One annotation is the chunk of the text (e.g. mutation mention)
        whose tokens have labels that are continuously not 'O'
        For example:
        ... O O O A D I S A O O O ...
        ... ----- annotation ---- ...
        here the text representing the tokens 'A, D, I, S, A' will be one predicted annotation (mention).
        Assumes that the 'O' label means outside of mention.

        Requires predicted_label[0].value for each token to be set.
        """
        for part_id, part in self.partids_with_parts():
            so_far = 0
            for sentence in part.sentences:
                index = 0
                while index < len(sentence):
                    token = sentence[index]
                    so_far = part.text.find(token.word, so_far)
                    confidence_values = []
                    if token.predicted_labels[0].value is not 'O':
                        start = so_far
                        confidence_values.append(token.predicted_labels[0].confidence)
                        while index + 1 < len(sentence) \
                                and sentence[index + 1].predicted_labels[0].value not in ('O', 'B', 'A'):
                            token = sentence[index + 1]
                            confidence_values.append(token.predicted_labels[0].confidence)
                            so_far = part.text.find(token.word, so_far)
                            index += 1
                        end = so_far + len(token.word)
                        confidence = aggregator_function(confidence_values)
                        part.predicted_annotations.append(Annotation(class_id, start, part.text[start:end], confidence))
                        # print(confidence, confidence_values)  TODO print debug
                    index += 1

    def clean_nl_definitions(self):
        """
        cleans all subclass = True to = False
        """
        for ann in self.annotations():
            ann.subclass = False

    def stats(self):
        """
        Calculates stats on the dataset. Like amount of nl mentions, ....
        """
        import re

        # main values
        nl_mentions = []  # array of nl mentions each of the the whole ann.text saved
        nl_nr = 0  # total nr of nl mentions
        nl_token_nr = 0  # total nr of nl tokens
        mentions_nr = 0  # total nr of all mentions (including st mentions)
        mentions_token_nr = 0  # total nr of all tokens of all mentions (inc st mentions)
        total_token_abstract = 0
        total_token_full = 0

        # abstract nr
        abstract_mentions_nr = 0
        abstract_token_nr = 0
        abstract_nl_mentions = []

        # full document nr
        full_document_mentions_nr = 0
        full_document_token_nr = 0
        full_nl_mentions = []

        # abstract and full document count
        abstract_doc_nr = 0
        full_doc_nr = 0

        # helper lists with unique pubmed ids that were already found
        abstract_unique_list = []
        full_unique_list = []

        # nl-docid set
        nl_doc_id_set = { 'empty' }

        # is abstract var
        is_abstract = True

        # precompile abstract match
        regex_abstract_id = re.compile(r'^s[12][shp]')

        for pubmedid, partid, ann in self.all_annotations_with_ids():
            # abstract?
            if regex_abstract_id.match(partid) or partid == 'abstract' or (len(partid) > 7 and partid[:8] == 'abstract'):
                # TODO #23 check for len(partid) > 7 and ... is enough for the out of index error handling
                is_abstract = True
            else:
                is_abstract = False

            if ann.class_id == MUT_CLASS_ID:
                # preprocessing
                token_nr = len(ann.text.split(" "))
                mentions_nr += 1
                mentions_token_nr += token_nr

                if ann.subclass:
                    # total nr increase
                    nl_nr += 1
                    nl_token_nr += token_nr

                    # min doc attribute
                    if pubmedid not in nl_doc_id_set:
                        nl_doc_id_set.add(pubmedid)

                    # abstract nr of tokens increase
                    if is_abstract:
                        abstract_mentions_nr += 1
                        abstract_token_nr += token_nr
                        abstract_nl_mentions.append(ann.text)
                    else:
                        # full document nr of tokens increase
                        full_document_mentions_nr += 1
                        full_document_token_nr += token_nr
                        full_nl_mentions.append(ann.text)

                    # nl text mention add to []
                    nl_mentions.append(ann.text)

        # post-processing for abstract vs full document tokens
        for doc_id, doc in self.documents.items():
            for partid, part in doc.parts.items():
                if regex_abstract_id.match(partid) or partid == 'abstract' or (len(partid) > 7 and partid[:8] == 'abstract'):
                    # OPTIONAL use nltk or different tokenizer
                    total_token_abstract += len(part.text.split(" "))
                    if doc_id not in abstract_unique_list:
                        abstract_doc_nr += 1
                        abstract_unique_list.append(doc_id)
                else:
                    total_token_full += len(part.text.split(" "))
                    if doc_id not in full_unique_list:
                        full_doc_nr += 1
                        full_unique_list.append(doc_id)

        report_dict = {
            'nl_mention_nr': nl_nr,
            'tot_mention_nr': mentions_nr,
            'nl_token_nr': nl_token_nr,
            'tot_token_nr': mentions_token_nr,
            'abstract_nl_mention_nr': abstract_mentions_nr,
            'abstract_nl_token_nr': abstract_token_nr,
            'abstract_tot_token_nr': total_token_abstract,
            'full_nl_mention_nr': full_document_mentions_nr,
            'full_nl_token_nr': full_document_token_nr,
            'full_tot_token_nr': total_token_full,
            'nl_mention_array': sorted(nl_mentions),
            'abstract_nr': abstract_doc_nr,
            'full_nr': full_doc_nr,
            'abstract_nl_mention_array': sorted(abstract_nl_mentions),
            'full_nl_mention_array': sorted(full_nl_mentions)
        }

        return report_dict


class Document:
    """
    Class representing a single document, for example an article from PubMed.

    :type parts: dict
    """

    def __init__(self):
        # NOTE are the parts generally ordered? concerning their true ordering from the original document?
        self.parts = OrderedDict()
        """
        parts the document consists of, encoded as a dictionary
        where the key (string) is the id of the part
        and the value is an instance of Part
        """

    def __eq__(self, other):
        return self.get_size() == other.get_size()

    def __lt__(self, other):
        return self.get_size() - other.get_size() < 0

    def __iter__(self):
        """
        when iterating through the document iterate through each part
        """
        for part_id, part in self.parts.items():
            yield part

    def key_value_parts(self):
        """yields iterator for partids"""
        for part_id, part in self.parts.items():
            yield part_id, part

    def get_unique_mentions(self):
        """:return: set of all mentions (standard + natural language)"""
        mentions = []
        for part in self:
            for ann in part.annotations:
                mentions.append(ann.text)

        return set(mentions)

    def get_size(self):
        """give back rough size log(lettres)*parts"""
        lettres = 0
        parts = 0
        for part in self:
            lettres += len(part.text)
            parts += 1

        return math.log2(lettres)*parts


class Part:
    """
    Represent chunks of text grouped in the document that for some reason belong together.
    Each part hold a reference to the annotations for that chunk of text.

    :type text: str
    :type sentences: list[list[Token]]
    :type annotations: list[Annotation]
    :type predicted_annotations: list[Annotation]
    """

    def __init__(self, text):
        self.text = text
        """the original raw text that the part is consisted of"""
        self.sentences = [[]]
        """
        a list sentences where each sentence is a list of tokens
        derived from text by calling Splitter and Tokenizer
        """
        self.annotations = []
        """the annotations of the chunk of text as populated by a call to Annotator"""
        self.predicted_annotations = []
        """
        a list of predicted annotations as populated by a call to form_predicted_annotations()
        this represent the prediction on a mention label rather then on a token level
        """

    def __iter__(self):
        """
        when iterating through the part iterate through each sentence
        """
        return iter(self.sentences)


class Token:
    """
    Represent a token - the smallest unit on which we perform operations.
    Usually one token represent one word from the document.

    :type word: str
    :type original_labels: list[Label]
    :type predicted_labels: list[Label]
    :type features: dict
    """

    def __init__(self, word):
        self.word = word
        """string value of the token, usually a single word"""
        self.original_labels = None
        """the original labels for the token as assigned by some implementation of Labeler"""
        self.predicted_labels = None
        """the predicted labels for the token as assigned by some learning algorightm"""
        self.features = FeatureDictionary()
        """
        a dictionary of features for the token
        each feature is represented as a key value pair:
        * [string], [string] pair denotes the feature "[string]=[string]"
        * [string], [float] pair denotes the feature "[string]:[float] where the [float] is a weight"
        """

    def __repr__(self):
        """
        print calls to the class Token will print out the string contents of the word
        """
        return self.word


class FeatureDictionary(dict):
    """
    Extension of the built in dictionary with the added constraint that
    keys (feature names) cannot be updated.

    If the key (feature name) doesn't end with "[number]" appends "[0]" to it.
    This is used to identify the position in the window for the feature.

    Raises an exception when we try to add a key that exists already.
    """

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError('feature name "{}" already exists'.format(key))
        else:
            if not re.search('\[-?[0-9]+\]$', key):
                key += '[0]'
            dict.__setitem__(self, key, value)


class Annotation:
    """
    Represent a single annotation, that is denotes a span of text which represents some entitity.

    :type class_id: str
    :type offset: int
    :type text: str
    :type subclass: int
    :type confidence: float
    """
    def __init__(self, class_id, offset, text, confidence=1):
        self.class_id = class_id
        """the id of the class or entity that is annotated"""
        self.offset = offset
        """the offset marking the beginning of the annotation in regards to the Part this annotation is attached to."""
        self.text = text
        """the text span of the annotation"""
        self.subclass = False
        """
        int flag used to further subdivide classes based on some criteria
        for example for mutations (MUT_CLASS_ID): 0=standard, 1=natural language, 2=semi standard
        """
        self.confidence = confidence
        """aggregated mention level confidence from the confidence of the tokens based on some aggregation function"""

    equality_operator = 'exact'
    """
    determines when we consider two annotations to be equal
    can be "exact" or "overlapping" or "exact_or_overlapping"
    """

    def __repr__(self):
        return '{0}(ClassID: "{self.class_id}", Offset: "{self.offset}", Text: "{self.text}", IsNL: "{self.subclass}")'.format(Annotation.__name__, self=self)

    def __eq__(self, other):
        # consider them a match only if class_id matches
        if self.class_id == other.class_id:
            exact = self.offset == other.offset and self.text == other.text
            overlap = self.offset <= (other.offset + len(other.text)) and (self.offset + len(self.text)) >= other.offset

            if self.equality_operator == 'exact':
                return exact
            elif self.equality_operator == 'overlapping':
                # overlapping means only the case where we have an actual overlap and not exact match
                return not exact and overlap
            elif self.equality_operator == 'exact_or_overlapping':
                # overlap includes the exact case so just return that
                return overlap
            else:
                raise ValueError('other must be "exact" or "overlapping" or "exact_or_overlapping"')
        else:
            return False


class Label:
    """
    Represents the label associated with each Token.

    :type value: str
    :type confidence: float
    """

    def __init__(self, value, confidence=None):
        self.value = value
        """string value of the label"""
        self.confidence = confidence
        """probability of being correct if the label is predicted"""

    def __repr__(self):
        return self.value


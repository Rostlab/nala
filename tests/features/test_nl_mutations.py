from unittest import TestCase

from nalaf.preprocessing.spliters import NLTKSplitter
from nalaf.preprocessing.tokenizers import TmVarTokenizer
from nalaf.structures.data import Dataset, Document, Part, Token

from nala.features.nl_mutations import NLMentionFeatureGenerator


class TestNLMentionFeatureGenerator(TestCase):
    @classmethod
    def setUpClass(cls):
        # create a sample dataset to test
        cls.dataset = Dataset()

        doc_id1 = Document()

        doc_id1.parts['t1'] = Part('This title blows your mind')

        text = str('This magic only exists in your dreams. To become reality, you have to work at it. '
                                   'Thr is only available with the residue threonine and a mutation, '
                                   'though things can change positions '
                                   'when adding some more replacements. Between me being sorry '
                                   'and you being an insertion.')
        doc_id1.parts['p1'] = Part(text.replace('\n',''))

        cls.dataset.documents['doc_id1'] = doc_id1

        NLTKSplitter().split(cls.dataset)
        TmVarTokenizer().tokenize(cls.dataset)

        cls.feature = NLMentionFeatureGenerator(thr=4)
        cls.feature.generate(dataset=cls.dataset)

    def test_generate(self):
        for sent in self.dataset.sentences():
            for tok in sent:
                print(tok.start, tok.features)
            print()

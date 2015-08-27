import unittest
from nala.structures.data import Dataset, Document, Part, Annotation
from nala.learning.evaluators import Evaluator, MentionLevelEvaluator
from nala.utils import MUT_CLASS_ID


class TestMentionLevelEvaluator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # create a sample dataset to test
        cls.dataset = Dataset()
        doc_1 = Document()

        text = '.... aaaa .... bbbb .... cccc .... dddd .... eeee .... ffff .... gggg .... hhhh .... jjjj'
        part_1 = Part(text)

        cls.dataset.documents['doc_1'] = doc_1
        doc_1.parts['part_1'] = part_1

        exact_1 = Annotation(MUT_CLASS_ID, 5, 'aaaa')
        exact_1.subclass = 1
        exact_2 = Annotation(MUT_CLASS_ID, 55, 'ffff')
        exact_2.subclass = 2
        exact_3 = Annotation(MUT_CLASS_ID, 75, 'hhhh')
        exact_3.subclass = 2

        overlap_1_1 = Annotation(MUT_CLASS_ID, 25, 'cccc')
        overlap_1_1.subclass = 1
        overlap_1_2 = Annotation(MUT_CLASS_ID, 26, 'cc')
        overlap_1_2.subclass = 1

        overlap_2_1 = Annotation(MUT_CLASS_ID, 32, '.. ddd')
        overlap_2_1.subclass = 2
        overlap_2_2 = Annotation(MUT_CLASS_ID, 36, 'ddd ...')
        overlap_2_2.subclass = 2

        overlap_3_1 = Annotation(MUT_CLASS_ID, 65, 'gggg')
        overlap_3_1.subclass = 1
        overlap_3_2 = Annotation(MUT_CLASS_ID, 62, '.. gggg ..')
        overlap_3_2.subclass = 2

        missing_1 = Annotation('e2', 45, 'eeee')
        missing_1.subclass = 1
        missing_2 = Annotation('e2', 84, 'jjjj')
        missing_2.subclass = 1

        spurios = Annotation('e2', 15, 'bbbb')
        spurios.subclass = 1

        part_1.annotations = [exact_1, exact_2, exact_3, overlap_1_1, overlap_2_1, overlap_3_1, missing_1, missing_2]
        part_1.predicted_annotations = [exact_1, exact_2, exact_3, overlap_1_2, overlap_2_2, overlap_3_2, spurios]

    def test_implements_evaluator_interface(self):
        self.assertIsInstance(MentionLevelEvaluator(), Evaluator)

    def test_exact_strictness(self):
        evaluator = MentionLevelEvaluator(strictness='exact')
        tp, fp, fn, tp_overlapping, precision, recall, f_measure = evaluator.evaluate(self.dataset)

        self.assertEqual(tp, 3)  # the 3 exact matches
        self.assertEqual(fp, 4)  # the 3 overlapping + 1 spurious
        self.assertEqual(fn, 5)  # the 3 overlapping + 2 missing

        self.assertEqual(precision, 3 / 7)
        self.assertEqual(recall, 3 / 8)
        self.assertEqual(f_measure, 2 * (3 / 7 * 3 / 8) / (3 / 7 + 3 / 8))

    def test_overlapping_strictness(self):
        evaluator = MentionLevelEvaluator(strictness='overlapping')
        tp, fp, fn, tp_overlapping, precision, recall, f_measure = evaluator.evaluate(self.dataset)

        self.assertEqual(tp, 3)  # the 3 exact matches
        self.assertEqual(fp, 1)  # the 1 spurious
        self.assertEqual(fn, 2)  # the 2 missing
        self.assertEqual(tp_overlapping, 3)  # the 3 overlapping

        self.assertEqual(precision, 6 / 7)
        self.assertEqual(recall, 6 / 8)
        self.assertEqual(f_measure, 2 * (6 / 7 * 6 / 8) / (6 / 7 + 6 / 8))

    def test_half_overlapping_strictness(self):
        evaluator = MentionLevelEvaluator(strictness='half_overlapping')
        tp, fp, fn, tp_overlapping, precision, recall, f_measure = evaluator.evaluate(self.dataset)

        self.assertEqual(tp, 3)  # the 3 exact matches
        self.assertEqual(fp, 1)  # the 1 spurious
        self.assertEqual(fn, 2)  # the 2 missing
        self.assertEqual(tp_overlapping, 3)  # the 3 overlapping

        self.assertEqual(precision, (3 + 3 / 2) / 7)
        self.assertEqual(recall, (3 + 3 / 2) / 8)
        self.assertEqual(f_measure, 2 * ((3 + 3 / 2) / 7 * (3 + 3 / 2) / 8) / ((3 + 3 / 2) / 7 + (3 + 3 / 2) / 8))

    def test_exception_on_equality_operator(self):
        ann_1 = Annotation(MUT_CLASS_ID, 1, 'text_1')
        ann_2 = Annotation(MUT_CLASS_ID, 2, 'text_2')

        Annotation.equality_operator = 'not valid'
        self.assertRaises(ValueError, lambda: ann_1 == ann_2)

    def test_exception_on_strictness(self):
        evaluator = MentionLevelEvaluator(strictness='not valid')

        self.assertRaises(ValueError, evaluator.evaluate, self.dataset)

    def test_subclass_analysis(self):
        evaluator = MentionLevelEvaluator(strictness='exact', subclass_analysis=True)
        subclass_counts, *_ = evaluator.evaluate(self.dataset)
        self.assertEqual(subclass_counts[1]['tp'], 1)
        self.assertEqual(subclass_counts[2]['tp'], 2)

        self.assertEqual(subclass_counts[1]['fp'], 2)
        self.assertEqual(subclass_counts[2]['fp'], 2)

        self.assertEqual(subclass_counts[1]['fn'], 4)
        self.assertEqual(subclass_counts[2]['fn'], 1)

        self.assertEqual(subclass_counts[1]['tp_overlapping'], 1)
        self.assertEqual(subclass_counts[2]['tp_overlapping'], 1)

if __name__ == '__main__':
    unittest.main()

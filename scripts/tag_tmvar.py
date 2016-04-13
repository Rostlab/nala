from nala.utils.corpora import get_corpus
from nala.learning.taggers import TmVarTagger
from nalaf.learning.evaluators import MentionLevelEvaluator
from nala.preprocessing.definers import ExclusiveNLDefiner
from nalaf.utils.writers import PubTatorFormat, TagTogFormat

data = get_corpus('SETH')


def predict():
    with TmVarTagger() as t:
        t.tag(data)

    TagTogFormat(data, use_predicted=True,
                 to_save_to='/home/abojchevski/projects/nala/resources/predictions/tmVar/').export_ann_json(1)


def evaluate():
    from nalaf.utils.annotation_readers import AnnJsonAnnotationReader
    print(len(data))
    AnnJsonAnnotationReader('/home/abojchevski/projects/nala/resources/predictions/tmVar/SETH',
                            is_predicted=True, delete_incomplete_docs=False).annotate(data)
    print(len(data))
    # for part in data.parts():
    #     print(sorted([a.text for a in part.annotations]))
    #     print(sorted([a.text for a in part.predicted_annotations]))
    #     print()
    ExclusiveNLDefiner().define(data)
    e = MentionLevelEvaluator(subclass_analysis=True).evaluate(data)
    print(e)


# predict()
evaluate()

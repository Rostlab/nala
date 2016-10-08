import sys
import os
from nala.utils.corpora import get_corpus, get_corpora
from nala.learning.taggers import TmVarTagger
from nalaf.learning.evaluators import MentionLevelEvaluator
from nala.preprocessing.definers import ExclusiveNLDefiner
from nalaf.utils.writers import TagTogFormat

# Example calls:
# python scripts/tag_tmvar.py nala_test resources/predictions/ predict
# python scripts/tag_tmvar.py nala_test resources/predictions/ evaluate &> resources/predictions/tmVar/nala_test/oresults.tsv

corpus_name = sys.argv[1]
preds_folder = sys.argv[2]
folder_name = os.path.join(preds_folder, 'tmVar', corpus_name)
is_predict = sys.argv[3] == "predict"  # anything else --> evaluate

data = get_corpora(corpus_name)

def predict():
    with TmVarTagger() as t:
        t.tag(data)

    TagTogFormat(data, use_predicted=True, to_save_to=folder_name).export_ann_json(1)


def evaluate():
    from nalaf.utils.annotation_readers import AnnJsonAnnotationReader
    size_before = len(data)
    AnnJsonAnnotationReader(os.path.join(folder_name, "annjson"), is_predicted=True, delete_incomplete_docs=False).annotate(data)
    assert(size_before == len(data))

    ExclusiveNLDefiner().define(data)
    e = MentionLevelEvaluator(subclass_analysis=True).evaluate(data)
    print(e)

if is_predict:
    predict()
else:
    evaluate()

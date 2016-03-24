import os
import pkg_resources
from nalaf.learning.taggers import Tagger
from nalaf.learning.crfsuite import PyCRFSuite
from nala.utils import MUT_CLASS_ID, get_prepare_pipeline_for_best_model
from nala.learning.postprocessing import PostProcessing
from nalaf import print_verbose, print_debug

class NalaSingleModelTagger(Tagger):

    def __init__(
    self,
    class_id = MUT_CLASS_ID,
    bin_model = pkg_resources.resource_filename('nala.data', 'all3_model'),
    features_pipeline = None,
    execute_pipeline = True):

        super().__init__([class_id])

        self.class_id = class_id
        self.bin_model = bin_model
        self.features_pipeline = features_pipeline if features_pipeline else get_prepare_pipeline_for_best_model()
        self.execute_pipeline = execute_pipeline
        #---
        self.crf = PyCRFSuite()
        self.post = PostProcessing()

    def tag(self, dataset):
        if self.execute_pipeline:
            self.features_pipeline.execute(dataset)
        self.crf.tag(dataset, self.bin_model, self.class_id)
        self.post.process(dataset)

class NalaTagger(Tagger):

    def __init__(
    self,
    class_id = MUT_CLASS_ID,
    st_model = pkg_resources.resource_filename('nala.data', 'st_model'),
    all3_model = pkg_resources.resource_filename('nala.data', 'all3_model'),
    features_pipeline = None):

        super().__init__([class_id])

        tagger1 = NalaSingleModelTagger(class_id, st_model, features_pipeline)
        tagger2 = NalaSingleModelTagger(class_id, all3_model, tagger1.features_pipeline, execute_pipeline = False)
        self.tagger = MultipleModelTagger(tagger1, tagger2, [class_id])
        #---
        self.post = PostProcessing()

    def tag(self, dataset):
        self.tagger.tag(dataset)
        self.post.process(dataset)


class MultipleModelTagger(Tagger):

    def __init__(
    self,
    tagger1,
    tagger2,
    predicts_classes):

        super().__init__(predicts_classes)

        self.tagger1 = tagger1
        self.tagger2 = tagger2

    def _clean_predictions(self, dataset, name = "tagger"):
        for part in dataset.parts():
            print_debug(name, [ann.text for ann in part.predicted_annotations])
            part.predicted_annotations = []

    def tag(self, dataset):
        import tempfile
        from nalaf.utils.writers import TagTogFormat
        from nalaf.utils.annotation_readers import AnnJsonMergerAnnotationReader, AnnJsonAnnotationReader
        """
        Current implementation uses annjsonmergerreader for merging annotations
        This is far from ideal. Dataset objects should be merged on memory.
        """

        tmpdir = tempfile.mkdtemp()

        self.tagger1.tag(dataset)
        TagTogFormat(dataset, tmpdir).export_ann_json()
        os.rename(tmpdir + '/annjson', tmpdir + '/tagger1_annjson')
        self._clean_predictions(dataset, "tagger1")

        self.tagger2.tag(dataset)
        TagTogFormat(dataset, tmpdir).export_ann_json()
        os.rename(tmpdir + '/annjson', tmpdir + '/tagger2_annjson')
        self._clean_predictions(dataset, "tagger2")

        AnnJsonMergerAnnotationReader(tmpdir, strategy='union', entity_strategy='priority',
        priority=['tagger1_annjson', 'tagger2_annjson'],
        delete_incomplete_docs=False, is_predicted=True).annotate(dataset)

        return dataset

import warnings
import difflib
import requests
import re
import os
import pkg_resources
from nalaf.learning.taggers import Tagger
from nalaf.learning.crfsuite import PyCRFSuite
from nalaf.structures.data import Entity
from nalaf.utils.cache import Cacheable

from nala.utils import MUT_CLASS_ID, get_prepare_pipeline_for_best_model
from nala.learning.postprocessing import PostProcessing
from nalaf import print_debug


class NalaSingleModelTagger(Tagger):
    def __init__(
            self,
            class_id=MUT_CLASS_ID,
            bin_model=pkg_resources.resource_filename('nala.data', 'all3_model'),
            features_pipeline=None,
            execute_pipeline=True,
            keep_silent=True,
            keep_genetic_markers=True,
            keep_unnumbered=True):

        super().__init__([class_id])

        self.class_id = class_id
        self.bin_model = bin_model
        self.features_pipeline = features_pipeline if features_pipeline else get_prepare_pipeline_for_best_model()
        self.execute_pipeline = execute_pipeline
        # ---
        self.crf = PyCRFSuite()
        self.post = PostProcessing(keep_silent=keep_silent,
                                   keep_genetic_markers=keep_genetic_markers,
                                   keep_unnumbered=keep_unnumbered)

    def tag(self, dataset):
        if self.execute_pipeline:
            self.features_pipeline.execute(dataset)
        self.crf.tag(dataset, self.bin_model, self.class_id)
        self.post.process(dataset)


class NalaMultipleModelTagger(Tagger):
    def __init__(
            self,
            class_id=MUT_CLASS_ID,
            st_model=pkg_resources.resource_filename('nala.data', 'st_model'),
            all3_model=pkg_resources.resource_filename('nala.data', 'all3_model'),
            features_pipeline=None,
            keep_silent=True,
            keep_genetic_markers=True,
            keep_unnumbered=True):

        super().__init__([class_id])

        tagger1 = NalaSingleModelTagger(class_id, st_model, features_pipeline)
        tagger2 = NalaSingleModelTagger(class_id, all3_model, tagger1.features_pipeline, execute_pipeline=False)
        self.tagger = MultipleModelTagger(tagger1, tagger2, [class_id])
        # ---
        self.post = PostProcessing(keep_silent=keep_silent,
                                   keep_genetic_markers=keep_genetic_markers,
                                   keep_unnumbered=keep_unnumbered)

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

    def _clean_predictions(self, dataset, name="tagger"):
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
        TagTogFormat(dataset, use_predicted=True, to_save_to=tmpdir).export_ann_json()
        os.rename(tmpdir + '/annjson', tmpdir + '/tagger1_annjson')
        self._clean_predictions(dataset, "tagger1")

        self.tagger2.tag(dataset)
        TagTogFormat(dataset, use_predicted=True, to_save_to=tmpdir).export_ann_json()
        os.rename(tmpdir + '/annjson', tmpdir + '/tagger2_annjson')
        self._clean_predictions(dataset, "tagger2")

        AnnJsonMergerAnnotationReader(tmpdir, strategy='union', entity_strategy='priority',
                                      priority=['tagger1_annjson', 'tagger2_annjson'],
                                      delete_incomplete_docs=False, is_predicted=True).annotate(dataset)

        return dataset


class TmVarTagger(Cacheable, Tagger):
    """
    The tagger doesn't work on any dataset as we cannot use the free-form text tmVar API at the moment.
    We default to the API that works only on PubMed abstracts.

    In general these are the 2 restrictions:

        1. doc_ic in the dictionary should be the pubmed ID
        2. the doc should have 2 parts, where the first part is the title and the second part is the abstract

    Any dataset that satisfies both of these should be taggable

    Note also that the official TmVar API doesn't work with title-only pubmed documents as PMID7175934
    (http://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/Mutation/7175934/Pubtator/)

    However, tmVar works with their other provided demo service:
    http://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/tmTools/demo/tmVar/
    """

    def __init__(self):
        Cacheable.__init__(self)
        Tagger.__init__(self, predicts_classes=[MUT_CLASS_ID])
        self.url_tmvar = 'http://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/Mutation/{}/Pubtator/'

    @staticmethod
    def __find_offset_adjustments(s1, s2):
        return [(i1, j2 - j1 - i2 + i1)
                for operation, i1, i2, j1, j2 in difflib.SequenceMatcher(None, s1, s2).get_opcodes()
                if operation in ['replace', 'insert']]

    def tag(self, data):
        """
        :type data: nalaf.structures.data.Dataset
        """
        for doc_id, doc in data.documents.items():
            if doc_id in self.cache:
                response_text = self.cache[doc_id]
            else:
                r = requests.get(self.url_tmvar.format(doc_id))
                if r.status_code == 200:
                    response_text = r.text
                    self.cache[doc_id] = response_text
                else:
                    continue

            if response_text.startswith('[Error]'):
                warnings.warn(response_text)
            else:
                lines = response_text.strip().splitlines()
                if len(lines) >= 2 and len(doc.parts) == 2:
                    tm_var_title = re.search('{}\|t\|(.*)'.format(doc_id), lines[0]).group(1)
                    tm_var_abstract = re.search('{}\|a\|(.*)'.format(doc_id), lines[1]).group(1)

                    parts = iter(doc.parts.values())
                    title = next(parts)
                    abstract = next(parts)

                    for line in lines[2:]:
                        _, start, end, _, _, _ = line.split('\t')
                        start = int(start)
                        end = int(end)

                        if 0 <= start < end <= len(tm_var_title):
                            part = title
                            tm_part = tm_var_title
                        else:
                            part = abstract
                            tm_part = tm_var_abstract
                            start -= len(tm_var_title) + 1
                            end -= len(tm_var_title) + 1

                        if part.text[start:end] != tm_part[start:end]:
                            adjustments = self.__find_offset_adjustments(part.text, tm_part)

                            for offset_start, offset_count in adjustments:
                                if start > offset_start:
                                    start -= offset_count
                                if end > offset_start:
                                    end -= offset_count

                        part.predicted_annotations.append(Entity(MUT_CLASS_ID, start, part.text[start:end]))

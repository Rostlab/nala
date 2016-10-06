import warnings
import difflib
import requests
import re
import os
import pkg_resources
import json
import time
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
            execute_pp=True,
            keep_silent=True,
            keep_genetic_markers=True,
            keep_unnumbered=True,
            keep_rs_ids=True):

        super().__init__([class_id])

        self.class_id = class_id
        self.bin_model = bin_model
        self.features_pipeline = features_pipeline if features_pipeline else get_prepare_pipeline_for_best_model()
        self.execute_pipeline = execute_pipeline
        # ---
        self.crf = PyCRFSuite()

        self.post = None
        if execute_pp:
            self.post = PostProcessing(keep_silent=keep_silent,
                                       keep_genetic_markers=keep_genetic_markers,
                                       keep_unnumbered=keep_unnumbered,
                                       keep_rs_ids=keep_rs_ids)

    def tag(self, dataset, class_id=None):
        class_id = self.class_id if class_id is None else class_id
        if self.execute_pipeline:
            self.features_pipeline.execute(dataset)

        self.crf.tag(dataset, self.bin_model, class_id)
        if self.post:
            self.post.process(dataset, class_id=class_id)


class NalaMultipleModelTagger(Tagger):
    def __init__(
            self,
            class_id=MUT_CLASS_ID,
            st_model=pkg_resources.resource_filename('nala.data', 'st_model'),
            all3_model=pkg_resources.resource_filename('nala.data', 'all3_model'),
            features_pipeline=None,
            execute_pp=True,
            keep_silent=True,
            keep_genetic_markers=True,
            keep_unnumbered=True,
            keep_rs_ids=True):

        super().__init__([class_id])

        tagger1 = NalaSingleModelTagger(class_id, st_model, features_pipeline)
        tagger2 = NalaSingleModelTagger(class_id, all3_model, tagger1.features_pipeline, execute_pipeline=False)
        self.tagger = MultipleModelTagger(tagger1, tagger2, [class_id])
        # ---
        self.post = None
        if execute_pp:
            self.post = PostProcessing(keep_silent=keep_silent,
                                       keep_genetic_markers=keep_genetic_markers,
                                       keep_unnumbered=keep_unnumbered,
                                       keep_rs_ids=keep_rs_ids)

    def tag(self, dataset, class_id=None):
        class_id = self.class_id if class_id is None else class_id
        self.tagger.tag(dataset, class_id)
        if self.post:
            self.post.process(dataset, class_id=class_id)


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
        from nalaf.utils.annotation_readers import AnnJsonMergerAnnotationReader
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
        self.url_tmvar_pmids = 'http://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/Mutation/{}/Pubtator/'
        self.url_tmvar_freetext = 'http://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/tmVar/Submit'

    @staticmethod
    def __find_offset_adjustments(s1, s2):
        return [(i1, j2 - j1 - i2 + i1)
                for operation, i1, i2, j1, j2 in difflib.SequenceMatcher(None, s1, s2).get_opcodes()
                if operation in ['replace', 'insert']]

    @staticmethod
    def _adjust_offsets(text1, text2, start, end):
        if text1[start:end] != text2[start:end]:
            adjustments = TmVarTagger.__find_offset_adjustments(text1, text2)

            for offset_start, offset_count in adjustments:
                if start > offset_start:
                    start -= offset_count
                if end > offset_start:
                    end -= offset_count

        return (start, end)

    @staticmethod
    def _is_pmid(x):
        return x.isdigit() or x.lower().startswith('pmid')

    @staticmethod
    def _parse_pubtator(doc_id, doc, response_text):
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

                start, end = TmVarTagger._adjust_offsets(part.text, tm_part, start, end)

                part.predicted_annotations.append(Entity(MUT_CLASS_ID, start, part.text[start:end]))

    @staticmethod
    def _parse_json(doc_id, doc, response_text):
        try:
            for pred_part in json.loads(response_text, strict=False):
                partid = pred_part['sourceid']
                part = doc.parts[partid]
                for pred in pred_part['denotations']:
                    start = pred['span']['begin']
                    end = pred['span']['end']

                    start, end = TmVarTagger._adjust_offsets(part.text, pred_part['text'], start, end)

                    part.predicted_annotations.append(Entity(MUT_CLASS_ID, start, part.text[start:end]))
        except:
            print("ERROR PARSING JSON", response_text)
            raise

    @staticmethod
    def _doc_to_json(doc):
        """
        tmVar API has many quirks to put it mildly.

        The sent JSON hast to be compressed in order to be understood as JSON and receive a JSON back.
        Furthermore, double quotes are note treated properly. That's why we replace them by simple apostrophes
        """

        ret = []
        for partid, part in doc.parts.items():
            text_for_tmvar_api = part.text.replace('"', "'")
            sub = {'sourcedb': 'undefined', 'sourceid': partid, 'text': text_for_tmvar_api}
            ret.append(sub)
        ret = json.dumps(ret, separators=(',', ':'))
        return ret

    def tag(self, data):
        """
        :type data: nalaf.structures.data.Dataset
        """
        for doc_id, doc in data.documents.items():
            if doc_id in self.cache:
                print_debug("Use cached response", doc_id)

                response_text = self.cache[doc_id]
            elif len(doc.parts) == 2 and self._is_pmid(doc_id):
                print_debug("Use PMID-based API", doc_id)

                r = requests.get(self.url_tmvar_pmids.format(doc_id))
                if r.status_code == 200:
                    response_text = r.text
                    self.cache[doc_id] = response_text
                else:
                    continue
            else:
                print_debug("Use free-text API", doc_id)

                r = requests.post(self.url_tmvar_freetext, self._doc_to_json(doc))

                if 'Receive' in r.url:
                    s = 501
                    while s == 501:
                        time.sleep(5)
                        s = requests.get(r.url)
                        response_text = s.text
                        s = s.status_code
                    response_text = '['+response_text+']'
                    self.cache[doc_id] = response_text
                else:
                    continue

            if response_text.startswith('[Error]'):
                warnings.warn(response_text)
            else:
                if response_text.startswith("["):
                    self._parse_json(doc_id, doc, response_text)
                else:
                    self._parse_pubtator(doc_id, doc, response_text)

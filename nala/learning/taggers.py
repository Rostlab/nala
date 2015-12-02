from nalaf.learning.taggers import Tagger, RelationExtractor
from nalaf.utils.ncbi_utils import GNormPlus
from nala.utils.uniprot_utils import Uniprot
from nalaf.structures.data import Entity, Relation
from nala.utils import MUT_CLASS_ID, PRO_CLASS_ID, PRO_REL_MUT_CLASS_ID, ENTREZ_GENE_ID, UNIPROT_ID


class CRFSuiteMutationTagger(Tagger):
    """
    Performs tagging with a binary model using CRFSuite

    :type crf_suite: nala.learning.crfsuite.CRFSuite
    """

    def __init__(self, predicts_classes, crf_suite, model_file='default_model'):
        super().__init__(predicts_classes)
        self.crf_suite = crf_suite
        """an instance of CRFSuite used to actually generate predictions"""
        self.model_file = model_file
        """path to the binary model used for generating predictions"""

    def tag(self, dataset):
        """
        :type dataset: nala.structures.data.Dataset
        """
        self.crf_suite.create_input_file(dataset, 'predict')
        self.crf_suite.tag('-m {} -i predict > output.txt'.format(self.model_file))
        self.crf_suite.read_predictions(dataset)


class GNormPlusGeneTagger(Tagger):
    """
    Performs tagging for genes with GNormPlus.
    Is able to add normalisations for uniprot as well.

    :type crf_suite: nala.learning.crfsuite.CRFSuite
    """

    def __init__(self):
        super().__init__([ENTREZ_GENE_ID, UNIPROT_ID])

    def tag(self, dataset, annotated=False, uniprot=False, process_only_abstract=True):
        """
        :type dataset: nala.structures.data.Dataset
        :param annotated: if True then saved into annotations otherwise into predicted_annotations
        """
        with GNormPlus() as gnorm:
            for doc_id, doc in dataset.documents.items():
                if process_only_abstract:
                    genes = gnorm.get_genes_for_pmid(doc_id, postproc=True)
                    if uniprot:
                        with Uniprot() as uprot:
                            list_of_ids = gnorm.uniquify_genes(genes)
                            genes_mapping = uprot.get_uniprotid_for_entrez_geneid(list_of_ids)
                    else:
                        genes_mapping = {}

                    # find the title and the abstract
                    parts = iter(doc.parts.values())
                    title = next(parts)
                    abstract = next(parts)

                    for start, end, text, gene_id in genes:
                        if 0 <= start < end <= len(title.text):
                            part = title
                        else:
                            part = abstract
                            # we have to readjust the offset since GnormPlus provides
                            # offsets for title and abstract together
                            offset = len(title.text) + 1
                            start -= offset
                            end -= offset

                        # todo discussion which confidence value for gnormplus because there is no value supplied
                        ann = Entity(class_id=PRO_CLASS_ID, offset=start, text=text, confidence=0.5)
                        try:
                            norm_dict = {
                                ENTREZ_GENE_ID: gene_id,
                                UNIPROT_ID: genes_mapping[gene_id]
                            }
                        except KeyError:
                            norm_dict = {ENTREZ_GENE_ID: gene_id}

                        norm_string = ''  # todo normalized_text (stemming ... ?)
                        ann.normalisation_dict = norm_dict
                        ann.normalized_text = norm_string
                        if annotated:
                            part.annotations.append(ann)
                        else:
                            part.predicted_annotations.append(ann)
                else:
                    # todo this is not used for now anywhere, might need to be re-worked or excluded
                    # genes = gnorm.get_genes_for_text(part.text)
                    pass


class StubSameSentenceRelationExtractor(RelationExtractor):
    def __init__(self):
        super().__init__(PRO_CLASS_ID, MUT_CLASS_ID, PRO_REL_MUT_CLASS_ID)

    def tag(self, dataset):
        from itertools import product
        for part in dataset.parts():
            for ann_1, ann_2 in product(
                    (ann for ann in part.predicted_annotations if ann.class_id == self.entity1_class),
                    (ann for ann in part.predicted_annotations if ann.class_id == self.entity2_class)):
                if part.get_sentence_index_for_annotation(ann_1) == part.get_sentence_index_for_annotation(ann_2):
                    part.predicted_relations.append(
                        Relation(ann_1.offset, ann_2.offset, ann_1.text, ann_2.text, PRO_REL_MUT_CLASS_ID))

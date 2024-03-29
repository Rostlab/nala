from nose.plugins.attrib import attr
from unittest import TestCase
from nalaf.utils.tagger import TmVarTagger
from nalaf.utils.ncbi_utils import GNormPlus
from nalaf.utils.annotation_readers import AnnJsonAnnotationReader
from nalaf.utils.readers import HTMLReader
from nala.utils.uniprot_utils import Uniprot
from nala.utils import MUT_CLASS_ID, PRO_CLASS_ID


__author__ = 'carst'


# todo major merge into tests/learning/test_taggers.py
@attr('slow')
class TestTmVarTagger(TestCase):
    def test_generate_abstracts(self):
        pmids = ['12559908']

        data = TmVarTagger(MUT_CLASS_ID).generate_abstracts(pmids)

        print(data)
        for docid in data.documents:
            print(data.documents[docid])


@attr('slow')
class TestGNormPlus(TestCase):
    def test_get_genes_for_pmid(self):
        pmid = '22457529'
        dataset = HTMLReader('resources/bootstrapping/iteration_0/base/html/').read()
        # AnnJsonAnnotationReader('resources/corpora/idp4/annjson').annotate(dataset)
        all_genes = []
        with GNormPlus() as gnorm:
            counter = 0
            for docid in dataset.documents:
                results = gnorm.get_genes_for_pmid(docid)
                print(counter)
                counter += 1
                if len(results) > 0:
                    genes = set([elem for sublist in results for elem in sublist[3].split(',')])
                    all_genes.extend(genes)
        unique_gene_set = set(all_genes)
        # "GeneID:114548"
        # "140859"
        # "GeneID:43829/PSSMID:210065"
        print(unique_gene_set)


@attr('slow')
class TestUniprot(TestCase):
    def test_get_uniprotid_for_entrez_geneid(self):
        with Uniprot() as uprot:
            uprot.get_uniprotid_for_entrez_geneid([4535, 1558079])

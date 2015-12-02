"""
nala.utils contains classes that help for instance with downloading doc- uments from the internet.
The import and export classes are contained there as well. Other classes are:
– Cacheprovidingcachingforclassesthatneedtodownloadstaticcontent often.
– GNormPlus which annotates either full-text documents or PubMed abstracts through the RESTApi from PubTator.
– Tagger which implements an easy interface to be able to use external taggers for example TmVarTagger, that can use PubTator as well, to download mutation mentions through the tmVar method.
– Uniprot helps with normalising EntrezGene IDs [22] to Uniprot IDs [23]. This is part of the normalisation process in class GNormPlusGeneTagger.
"""

PRO_CLASS_ID = 'e_1'
MUT_CLASS_ID = 'e_2'
ORG_CLASS_ID = 'e_3'
PRO_REL_MUT_CLASS_ID = 'r_4'  # e_1/e_2
PRO_REL_ORG_CLASS_ID = 'r_5'  # e_1/e_3
THRESHOLD_VALUE = 1
ENTREZ_GENE_ID = 'n_4'
UNIPROT_ID = 'n_5'
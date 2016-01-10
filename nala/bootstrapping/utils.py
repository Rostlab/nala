from itertools import chain
from xml.etree import ElementTree as ET
import requests
from nalaf.structures.data import Document, Part
from nalaf.utils.cache import Cacheable

__author__ = 'Aleksandar'


class UniprotDocumentSelector(Cacheable):
    """
    Selects a list of pubmed IDs (articles) that are likely to have mutation mentions.

    Outline of the selection procedure:
    1. Select proteins given a uniprot query (by default Swiss-Prot human proteins)
    2. For each protein search for articles showing evidence of sequence variant of mutagenesis
    3. Return pubmed IDs (articles) associated with the evidence
    """

    def __init__(self):
        super().__init__()
        self.processed = set()
        self.uniprot_url = 'http://www.uniprot.org/uniprot/'

    def _get_uniprot_ids(self, query=None):
        if not query:
            query = '(annotation:(type:natural_variations) OR annotation:(type:mutagen))' \
                    ' AND reviewed:yes AND organism:"Homo sapiens (Human) [9606]"'
        params = {'query': query,
                  'columns': 'id',
                  'format': 'tab'}

        if query in self.cache:
            lines = self.cache[query]
        else:
            req = requests.get(self.uniprot_url, params)
            lines = req.text.splitlines()
            self.cache[query] = lines

        for uniprot_id in lines[1:]:  # skip first line
            yield uniprot_id

    def _get_pubmed_ids_for_protein(self, uniprot_id):
        if uniprot_id in self.cache:
            text = self.cache[uniprot_id]
        else:
            req = requests.get(self.uniprot_url + '{}.xml'.format(uniprot_id))
            text = req.text
            self.cache[uniprot_id] = text

        xml = ET.fromstring(text)
        ns = {'u': 'http://uniprot.org/uniprot'}  # namespace

        evidence_ids = []
        for elem in xml.findall('.//u:feature[@evidence]', ns):
            if elem.attrib['type'] in ('sequence variant', 'mutagenesis site'):
                evidence_ids += elem.attrib['evidence'].split(' ')

        for evidence_id in evidence_ids:
            for elem in xml.findall(
                    './/u:evidence[@key="{}"]/u:source/u:dbReference[@type="PubMed"]'.format(evidence_id), ns):
                pubmed_id = elem.attrib['id']
                # check to see if we have seen this id before
                if pubmed_id not in self.processed:
                    self.processed.add(pubmed_id)
                    yield pubmed_id

    def get_pubmed_ids(self):
        for uniprot_id in self._get_uniprot_ids():
            for pubmed_id in self._get_pubmed_ids_for_protein(uniprot_id):
                yield pubmed_id

from nalaf.features import FeatureGenerator
import re


class SemiStandardFeatureGenerator(FeatureGenerator):
    """

    """

    def __init__(self):
        self.exon_intron_position = re.compile(
            '(in|into|of|by|end of|out of frame|out-of-frame|in frame|in-frame)?'
            ' *(exons?|introns?)'
            ' *\d+'
            '( *(and|or) *\d+)?')

        self.normal_position = re.compile(
            '(at|in|of|on|)'
            '( *the)?'
            ' *(positions?|amino acids?|codons?|nucleotides?|residues?|)'
            ' *\d+( *th)?')

        self.mutation_word = re.compile(
            '(substituted|substitutions?|transversions?|'
            'replacements?|replaced?|'
            'insertion|introducing|introduction|'
            'convert(ed|ing|s)?|conversions?)'
            '( *(of|at|by|in|into|on|an|to|between|with|a|each))?')

        self.amino_acids = [
            'alanine', 'ala', 'arginine', 'arg', 'asparagine', 'asn', 'aspartic acid', 'aspartate', 'asp',
            'cysteine', 'cys', 'glutamine', 'gln', 'glutamic acid', 'glutamate', 'glu', 'glycine', 'gly',
            'histidine', 'his', 'isoleucine', 'ile', 'leucine', 'leu', 'lysine', 'lys', 'methionine', 'met',
            'phenylalanine', 'phe', 'proline', 'pro', 'serine', 'ser', 'threonine', 'thr', 'tryptophan', 'trp',
            'tyrosine', 'tyr', 'valine', 'val', 'aspartic acid', 'asparagine', 'asx', 'glutamine', 'glutamic acid', 'glx']

    def generate(self, dataset):
        """
        :type dataset: nalaf.structures.data.Dataset
        """
        for part in dataset.parts():
            for sentence in part.sentences:
                joined_sentence = part.text[sentence[0].start:sentence[-1].start + len(sentence[-1].word)].lower()

                # find either of these 2 types of position mention
                position = None
                match = self.exon_intron_position.search(joined_sentence)
                if match:
                    position = match.span()
                else:
                    match = self.normal_position.search(joined_sentence)
                    if match and not match.group(0).strip().isnumeric():
                        position = match.span()

                # if there is a position mention and a mutation word tag the matched tokens
                match = self.mutation_word.search(joined_sentence)
                if position and match:
                    start_p, end_p = position
                    start_m, end_m = match.span()

                    # since we are working with sentences and not parts add the offset of the first token
                    start_p += sentence[0].start
                    end_p += sentence[0].start
                    start_m += sentence[0].start
                    end_m += sentence[0].start

                    for token in sentence:
                        if start_p <= token.start < token.end <= end_p:
                            token.features['semi_standard'] = 'pos'
                        if start_m <= token.start < token.end <= end_m:
                            token.features['semi_standard'] = 'word'
                        if token.word.lower() in self.amino_acids:
                            token.features['semi_standard'] = 'aa'

class NLMentionFeatureGenerator(FeatureGenerator):
    """
    Feature Generator that uses dictionaries of regular expressions to find possible nl mentions.
    Each of the dictionaries found position in the text in proximity to another dictionary
    will return a positive binary feature.

    Can be varied as well. (instead of binary make continuous or discrete scale)
    """

    def __init__(self):
        self.exon_intron_position = re.compile(
            '(in|into|of|by|end of|out of frame|out-of-frame|in frame|in-frame)?'
            ' *(exons?|introns?)'
            ' *\d+'
            '( *(and|or) *\d+)?')

        self.normal_position = re.compile(
            '(the)?'
            '(positions?|amino acids?|codons?|nucleotides?|residues?)'
            '\d+(\s*th)?')

        self.indicative_word = re.compile(
                'codon(s)|substitution(s)|substitut(s|ed)|amino acid(s)|'
                'nucleotide(s)|deletion(s)|delet(s|ed)|'
                'base(s) change(s|d)|base(s)|termination codon(s)|'
                'insertion(s)|insert(s|ed)|residue(s)|region(s)|'
                'duplication(s)|duplicate(d|s)|frameshift(s)|'
                'transversion(s)|exon(s)|termin(al|us)|position(s|ed)|'
                'phosphorylation site(s)|SNP(s)|upstream|'
                'downstream|replacement(s)|replace(s|d)|conserve(s|d)|'
                'transition(s)|miss(es|ing)|intron(s)'
        )

        self.connecting_word = re.compile(
            '(of|at|by|in|into|on|an|to|between|with|a|each)'
        )

        self.amino_acids = re.compile(
            '(cys|ile|ser|gln|met|asn|pro|lys|asp|thr|phe|ala|gly|his|leu|arg|trp|val|glu|tyr|glutamine|glutamic acid|'
            'leucine|valine|isoleucine|lysine|alanine|glycine|aspartate|methionine|threonine|histidine|aspartic acid|'
            'arginine|asparagine|tryptophan|proline|phenylalanine|cysteine|serine|glutamate|tyrosine)'
        )

        self.amino_acids_strings = [
            'alanine', 'ala', 'arginine', 'arg', 'asparagine', 'asn', 'aspartic acid', 'aspartate', 'asp',
            'cysteine', 'cys', 'glutamine', 'gln', 'glutamic acid', 'glutamate', 'glu', 'glycine', 'gly',
            'histidine', 'his', 'isoleucine', 'ile', 'leucine', 'leu', 'lysine', 'lys', 'methionine', 'met',
            'phenylalanine', 'phe', 'proline', 'pro', 'serine', 'ser', 'threonine', 'thr', 'tryptophan', 'trp',
            'tyrosine', 'tyr', 'valine', 'val', 'aspartic acid', 'asparagine', 'asx', 'glutamine', 'glutamic acid', 'glx']

    def generate(self, dataset):
        """
        :type dataset: nalaf.structures.data.Dataset
        """
        for part in dataset.parts():
            for sentence in part.sentences:
                joined_sentence = part.text[sentence[0].start:sentence[-1].start + len(sentence[-1].word)].lower()

                # find either of these 2 types of position mention
                position = None
                match = self.exon_intron_position.search(joined_sentence)
                if match:
                    position = match.span()
                else:
                    match = self.normal_position.search(joined_sentence)
                    if match and not match.group(0).strip().isnumeric():
                        position = match.span()

                # if there is a position mention and a mutation word tag the matched tokens
                match = self.mutation_word.search(joined_sentence)
                if position and match:
                    start_p, end_p = position
                    start_m, end_m = match.span()

                    # since we are working with sentences and not parts add the offset of the first token
                    start_p += sentence[0].start
                    end_p += sentence[0].start
                    start_m += sentence[0].start
                    end_m += sentence[0].start

                    for token in sentence:
                        if start_p <= token.start < token.end <= end_p:
                            token.features['semi_standard'] = 'pos'
                        if start_m <= token.start < token.end <= end_m:
                            token.features['semi_standard'] = 'word'
                        if token.word.lower() in self.amino_acids:
                            token.features['semi_standard'] = 'aa'

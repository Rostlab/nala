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

    def __init__(self, thr=4):
        """
        Init with regular expressions.
        Positional (exon-intron/normal)
        Indicative words (e.g. inseration)
        Connecting words (non-regex)
        Amino acids (non-regex)
        :param thr: sets the boundary of check for neighboring words
        """
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

        self.connecting_words = ['of', 'at', 'by', 'in', 'into', 'on', 'an', 'to', 'between', 'with', 'a', 'each',
                                 'from', 'which', 'the', 'without',
                                 'is', 'was', 'were', 'been', 'have', 'having', 'for', 'that', 'than', 'this', 'these',
                                 'its', 'rather', 'not', 'non', 'through', 'but']

        self.threshold = thr
        # self.amino_acids = re.compile(
        #     '(cys|ile|ser|gln|met|asn|pro|lys|asp|thr|phe|ala|gly|his|leu|arg|trp|val|glu|tyr|glutamine|glutamic acid|'
        #     'leucine|valine|isoleucine|lysine|alanine|glycine|aspartate|methionine|threonine|histidine|aspartic acid|'
        #     'arginine|asparagine|tryptophan|proline|phenylalanine|cysteine|serine|glutamate|tyrosine)'
        # )

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

                # position
                position = None
                match = self.exon_intron_position.search(joined_sentence)
                if match:
                    position = match.span()
                else:
                    match = self.normal_position.search(joined_sentence)
                    if match and not match.group(0).strip().isnumeric():
                        position = match.span()

                # helping array
                ta = ['' for _ in sentence]

                # match for position
                if match:
                    start_p, end_p = position

                    start_p += sentence[0].start
                    end_p += sentence[0].start

                    for i, token in enumerate(sentence):
                        if start_p <= token.start < token.end <= end_p:
                            token.features['nl_dict'] = 'pos'
                            ta[i] = 'pos'

                # indicative word
                matches = []
                for match in self.indicative_word.finditer(joined_sentence):
                    matches.append(match.span())

                if len(matches) > 0:
                    for i, token in enumerate(sentence):
                        for match in matches:
                            start_m, end_m = match

                            start_m += sentence[0].start
                            end_m += sentence[0].start

                            if start_m <= token.start < token.end <= end_m:
                                token.features['nl_dict'] = 'word'
                                ta[i] = 'word'

                # amino acids and connecting words
                for i, token in enumerate(sentence):
                    if token.word.lower() in self.amino_acids:
                        token.features['nl_dict'] = 'aa'
                        ta[i] = 'aa'
                    if token.word.lower() in self.connecting_words:
                        token.features['nl_dict'] = 'con'
                        ta[i] = 'con'

                ta_prox = [[] for _ in sentence]
                for i in range(len(ta)):
                    for k in range(i - self.threshold, i + self.threshold + 1):
                        if 0 <= k < len(ta) and ta[i]:
                            ta_prox[k].append(ta[i])

                for i, tok in enumerate(sentence):
                    ta_raw = [ti for ti in ta_prox[i] if ti != '']
                    if len(ta_raw) > 0:
                        ta_ocon = [t for t in ta_raw if t != 'con']
                        ta_word = [t for t in ta_raw if t == 'word']
                        ta_aa = [t for t in ta_raw if t == 'aa']
                        ta_pos = [t for t in ta_raw if t == 'pos']
                        feature_str = '-'.join(sorted(ta_raw))
                        feature_str_easy = '-'.join(sorted(list(set(ta_raw))))
                        feature_str_hard = '-'.join(ta_raw)
                        tok.features['nl_prox'] = feature_str
                        tok.features['nl_easy'] = feature_str_easy
                        tok.features['nl_hard'] = feature_str_hard
                        if any(ta_ocon):
                            tok.features['nl_no_con'] = True
                            tok.features['nl_hard_ocon'] = '-'.join(ta_ocon)
                        if any(ta_word) and any(ta_aa):
                            tok.features['nl_aa_word'] = True
                        if any(ta_word) and any(ta_pos):
                            tok.features['nl_pos_word'] = True
                    else:
                        tok.features['nl_prox'] = False

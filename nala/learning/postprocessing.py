import pkg_resources
import csv
import re
from nalaf.structures.data import Entity

from nala.preprocessing.definers import ExclusiveNLDefiner
from nala.utils import MUT_CLASS_ID


class PostProcessing:
    def __init__(self, keep_silent=True):
        amino_acids = [
            'alanine', 'ala', 'arginine', 'arg', 'asparagine', 'asn', 'aspartic acid', 'aspartate', 'asp',
            'cysteine', 'cys', 'glutamine', 'gln', 'glutamic acid', 'glutamate', 'glu', 'glycine', 'gly',
            'histidine', 'his', 'isoleucine', 'ile', 'leucine', 'leu', 'lysine', 'lys', 'methionine', 'met',
            'phenylalanine', 'phe', 'proline', 'pro', 'serine', 'ser', 'threonine', 'thr', 'tryptophan', 'trp',
            'tyrosine', 'tyr', 'valine', 'val', 'aspartic acid', 'asparagine', 'asx', 'glutamine', 'glutamic acid',
            'glx']

        keywords = ['substit\w*', 'lead\w*', 'exchang\w*', 'chang\w*', 'mutant\w*', 'mutate\w*', 'devia\w*', 'modif\w*',
                    'alter\w*', 'switch\w*', 'variat\w*', 'instead\w*', 'replac\w*', 'in place', 'convert\w*',
                    'becom\w*']

        self.patterns = [
            re.compile('({AA})[- ]*[1-9][0-9]* +(in|to|into|for|of|by|with|at) +({AA})( *(,|,?or|,?and) +({AA}))*'
                       .format(AA='|'.join(amino_acids)), re.IGNORECASE),
            re.compile('({AA}) +(in|to|into|for|of|by|with|at) +({AA})[- ]*[1-9][0-9]*'
                       '( *(,|,?or|,?and) +({AA})[- ]*[1-9][0-9]*)*'
                       .format(AA='|'.join(amino_acids)), re.IGNORECASE),
            re.compile('({AA})(( (({SS})) (in|to|into|for|of|by|with|at) (a|an|the|) '
                       '*({AA})[1-9]\d*( *(,|or|and|, and|, or) ({AA})[1-9]\d*)*)'
                       '|([- ]*[1-9]\d*( +((has|have|had) +been|is|are|was|were|) '
                       '+(({SS})))? +(in|to|into|for|of|by|with|at) +({AA})( *(,|or|and|, and|, or) +({AA}))*))'
                       .format(AA='|'.join(amino_acids), SS='|'.join(keywords)), re.IGNORECASE),
            re.compile(r'\bp\. *({AA}) *[-+]*\d+ *({AA})\b'.format(AA='|'.join(amino_acids)), re.IGNORECASE),
            re.compile(r'\b({AA})[-to ]*[-+]*\d+[-to ]*({AA})\b'.format(AA='|'.join(amino_acids)), re.IGNORECASE),
            re.compile(r'\b\[?rs\]? *\d{2,}(,\d+)*\b', re.IGNORECASE),
            re.compile(r'\b(c\. *)?[ATCG] *([-+]|\d)\d+ *[ATCG]\b'),
            re.compile(r'\b(c\.|E(X|x)\d+) *([-+]|\d)\d+[ATCG] *> *[ATCG]\b'),
            re.compile(r'\b[ATCG](/|-|-*>|→|)[ATCG] *[-+]*[0-9]+\b'),
            re.compile(r'\b[-+]*\d+ *(b|bp|N|ntb|p|BP|B) *(INS|DEL|INDEL|DELINS|DUP|ins|del|indel|delins|dup)\b'),
            re.compile(r'\b[^\x00-\x7F]?[-+]*\d+ *(INS|DEL|INDEL|DELINS|DUP|ins|del|indel|delins|dup)[0-9ATCGU]+\b'),
            re.compile(r'\b[ATCG]+ *[-+]*\d+ *(INS|DEL|INDEL|DELINS|DUP|ins|del|indel|delins|dup)\b'),
            re.compile(r'\b(INS|DEL|INDEL|DELINS|DUP|ins|del|indel|delins|dup) *(\d+(b|bp|N|ntb|p|BP|B)|[ATCG]{2,})\b'),
            re.compile(r'\b[-+]?\d+ *\d+ *(b|bp|N|ntb|p|BP|B) *(INS|DEL|INDEL|DELINS|DUP|ins|del|indel|delins|dup)\b'),
            re.compile(r'\b[-+]*\d+ *(INS|DEL|INDEL|DELINS|DUP|ins|del|indel|delins|dup)[A-Z]+\b'),
            re.compile(r'\b[^\x00-\x7F]?[CISQMNPKDTFAGHLRWVEYX] *\d{2,} *[CISQMNPKDTFAGHLRWVEYX]'
                       r'( *(/) *[CISQMNPKDTFAGHLRWVEYX])*\b'),
            re.compile(r'\b[CISQMNPKDTFAGHLRWVEYX]+ *[-+]*\d+ *(INS|DEL|INDEL|DELINS|DUP|ins|del|indel|delins|dup)\b'),
            re.compile(r'\b[ATCG][-+]*\d+[ATCG]/[ATCG]\b')
        ]

        self.negative_patterns = [
            # single AAs
            re.compile('^({AA}) *\d+$'.format(AA='|'.join(amino_acids)), re.IGNORECASE),
            re.compile('^[CISQMNPKDTFAGHLRWVEYX]+ *\d+$'),
            re.compile('^({AA})([-/>]({AA}))*$'
                       .format(AA='|'.join(amino_acids + [aa for aa in 'CISQMNPKDTFAGHLRWVEYX'])), re.IGNORECASE),
            # just numbers
            re.compile('^[-+]?\d+([-+/ ]+\d+)*( *(b|bp|N|ntb|p|BP|B))?$')
        ]

        self.at_least_one_letter_n_number_letter_n_number = re.compile('(?=.*[A-Za-z])(?=.*[0-9])[A-Za-z0-9]+')
        self.keep_silent = keep_silent
        self.definer = ExclusiveNLDefiner()

    def process(self, dataset, class_id=MUT_CLASS_ID):
        for doc_id, doc in dataset.documents.items():
            for part_id, part in doc.parts.items():
                self.__fix_issues(part)
                for regex in self.patterns:
                    for match in regex.finditer(part.text):
                        start = match.start()
                        end = match.end()
                        matched_text = part.text[start:end]
                        ann = Entity(class_id, start, matched_text)

                        Entity.equality_operator = 'exact_or_overlapping'
                        if ann not in part.predicted_annotations:
                            part.predicted_annotations.append(Entity(class_id, start, matched_text))
                        Entity.equality_operator = 'overlapping'
                        if ann in part.predicted_annotations:
                            for index, ann_b in enumerate(part.predicted_annotations):
                                if ann == ann_b and len(matched_text) > len(ann_b.text):
                                    part.predicted_annotations[index] = ann

                to_delete = [index for index, ann in enumerate(part.predicted_annotations)
                             if any(r.search(ann.text) for r in self.negative_patterns)
                             or (not self.keep_silent and self.__is_silent(ann))]

                part.predicted_annotations = [ann for index, ann in enumerate(part.predicted_annotations)
                                              if index not in to_delete]

    def __is_silent(self, ann):
        split = re.split('[-+]?[\d]+', ann.text)
        return len(split) == 2 and split[0] == split[1]

    def __fix_issues(self, part):
        to_be_removed = []
        for index, ann in enumerate(part.predicted_annotations):
            start = ann.offset
            end = ann.offset + len(ann.text)

            # split multiple mentions
            if re.search(r' *(?:\band\b|/|\\|,|;|\bor\b) *', ann.text):
                split = re.split(r' *(?:\band\b|/|\\|,|;|\bor\b) *', ann.text)

                # for each split part calculate the offsets and the constraints
                offset = 0
                split_info = []
                for text in split:
                    split_info.append((text, self.definer.define_string(text), ann.text.find(text, offset),
                                       self.at_least_one_letter_n_number_letter_n_number.search(text)))
                    offset += len(text)

                # if all the non empty parts are from class ST (0) and also contain at least one number and one letter
                if all(split_part[1] == 0 and split_part[3] for split_part in split_info if split_part[0] != ''):
                    to_be_removed.append(index)

                    # add them to
                    for split_text, split_class, split_offset, aonanl in split_info:
                        if split_text != '':
                            part.predicted_annotations.append(
                                Entity(ann.class_id, ann.offset + split_offset, split_text))

            # fix boundary #17000021	251	258	1858C>T --> +1858C>T
            if re.search('^[0-9]', ann.text) and re.search('([\-\+])', part.text[start - 1]):
                ann.offset -= 1
                ann.text = part.text[start - 1] + ann.text

            # fix boundary delete (
            if ann.text[0] == '(' and ')' not in ann.text:
                ann.offset += 1
                ann.text = ann.text[1:]

            # fix boundary delete )
            if ann.text[-1] == ')' and '(' not in ann.text:
                ann.text = ann.text[:-1]

            # fix boundary add missing (
            if part.text[start - 1] == '(' and ')' in ann.text:
                ann.offset -= 1
                ann.text = '(' + ann.text

            # fix boundary add missing )
            try:
                if part.text[end] == ')' and '(' in ann.text:
                    ann.text += ')'
            except IndexError:
                pass

            # fix boundary add missing number after fsX
            try:
                if ann.text.endswith('fs') or ann.text.endswith('fsX'):
                    tmp = end
                    if not ann.text.endswith('X') and part.text[tmp] == 'X':
                        ann.text += 'X'
                        tmp += 1
                    while part.text[tmp].isnumeric():
                        ann.text += part.text[tmp]
                        tmp += 1
            except IndexError:
                pass

            isword = re.compile("\\w")

            # The word must end in space to the left
            while ann.offset > 0 and isword.search(part.text[ann.offset - 1]):
                ann.text = part.text[ann.offset - 1] + ann.text
                ann.offset -= 1

            veryend = len(ann.text)
            end = ann.offset + len(ann.text)

            # The word must end in space to the right
            while end < veryend and isword.search(part.text[end]):
                ann.text = ann.text + part.text[end]
                end += 1

            # Remove parenthesis if within parenthesis but no parentesis either in between
            if ann.text[0] in ['('] and ann.text[-1] in [')'] and (ann.text.count('(') < 2 and ann.text.count(')') < 2):
                ann.offset += 1
                ann.text = ann.text[1:-1]

            # Follow the rule of abbreviations + first gene mutation (then protein mutation)
            if ((ann.text[-1] == ')' or (end < veryend and part.text[end] == ")")) and ann.text[:-1].count('(') == 1):
                p = re.compile("\\s+\\(")
                split = p.split(ann.text)

                # Requirement 1: must be space to the left of (, not to match things like in Arg407(AGG) or IVS3(+1)
                # Requirement 2: both parths must contain a number (both parts contain a position and can stand alone)
                #   Negative: Arg407(AGG) - single amino acid substitution (Phe for Val) - nonsense mutation (286T)
                #   Negative: deletion (229bp) -  nonsense mutation (glycine 568 to stop)
                #   Negative: one insertion mutation (698insC) - AChR epsilon (CHRNE E376K)
                #
                #   Positive: serine to arginine at the codon 113 (p. S113R)
                #   Positive: mutagenesis of the initial ATG codon to ACG (Met 1 to Thr) - H2A at position 105 (Q105)
                #   Positive: Trp replacing Gln in position 156 (A*2406) - A-1144-to-C transversion (K382Q)
                #   Positive: deletion of 123 bases (41 codons) - exon 12 (R432T)
                if len(split) == 2 and any(c.isdigit() for c in split[1]):  # any(c.isdigit() for c in split[0])
                    ann1text = split[0]
                    to_be_removed.append(index)
                    part.predicted_annotations.append(Entity(ann.class_id, ann.offset, ann1text))
                    ann2text = split[1] if ann.text[-1] != ')' else split[1][:-1]
                    # last part is number of spaces + (
                    ann2offset = ann.offset + len(ann1text) + (len(ann.text) - sum(len(x) for x in split))
                    part.predicted_annotations.append(Entity(ann.class_id, ann2offset, ann2text))


        part.predicted_annotations = [ann for index, ann in enumerate(part.predicted_annotations)
                                      if index not in to_be_removed]


def construct_regex_patterns_from_predictions(dataset):
    """
    :type dataset: nalaf.structures.data.Dataset
    """
    regex_patterns = []
    for ann in dataset.predicted_annotations():
        item = ann.text
        # escape special regex characters
        item = item.replace('.', '\.').replace('+', '\+').replace(')', '\)').replace('(', '\(').replace('*', '\*')

        # numbers pattern
        item = re.sub('[0-9]+', '[0-9]+', item)

        # take care of special tokens
        item = re.sub('(IVS|EX)', '@@@@', item)
        item = re.sub('(rs|ss)', '@@@', item)

        # letters pattern
        item = re.sub('[a-z]', '[a-z]', item)
        item = re.sub('[A-Z]', '[A-Z]', item)

        # revert back special tokens
        item = re.sub('@@@@', '(IVS|EX)', item)
        item = re.sub('@@@', '(rs|ss)', item)

        # append space before and after the constructed pattern
        regex_patterns.append(re.compile(r'( |rt)({}) '.format(item)))

    base_regex = r'\b(rt)?({})\b'
    # include already prepared regex patterns
    # modified by appending space before and after the original pattern
    with open(pkg_resources.resource_filename('nala.data', 'RegEx.NL')) as file:
        for regex in csv.reader(file, delimiter='\t'):
            if regex[0].startswith('(?-xism:'):
                try:
                    regex_patterns.append(re.compile(base_regex.format(regex[0].replace('(?-xism:', '')),
                                                     re.VERBOSE | re.IGNORECASE | re.DOTALL | re.MULTILINE))
                except Exception as e:
                    if e.args[0] == 'sorry, but this version only supports 100 named groups':
                        # if the exception is due to too many named groups
                        # make the groups unnamed since we don't need them to be named in the frist place
                        fixed = regex[0].replace('(?-xism:', '')
                        fixed = re.sub('\((?!\?:)', '(?:', fixed)
                        regex_patterns.append(re.compile(base_regex.format(fixed)))


            else:
                regex_patterns.append(re.compile(base_regex.format(regex[0])))

    # add our own custom regex
    regex_patterns.append(re.compile(base_regex.format('[ATCG][0-9]+[ATCG]/[ATCG]')))

    return regex_patterns

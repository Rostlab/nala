import unittest

from nala.preprocessing.definers import ExclusiveNLDefiner

class TestNLDefiner(unittest.TestCase):
    def test_define(self):
        pass  # TODO

class TestInclusiveNLDefiner(unittest.TestCase):

    def test_init__(self):
        pass  # TODO

    def define(self):
        pass  # TODO


class TestAnkitNLDefiner(unittest.TestCase):

    def test_init(self):
        pass  # TODO

    def test_define(self):
        pass  # TODO


class TestExclusiveNLDefiner(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.definer = ExclusiveNLDefiner()

    def test_on_empty_string(self):
        try:
            self.definer.define_string("")
        except Exception:
            self.fail("empty string result is undefined but should not throw an exception")

    def test_define_string(self):
        f = self.definer.define_string
        testEqual = self.assertEqual

        testEqual(2, f("C226 to T"))
        testEqual(2, f("G446 to A"))
        testEqual(2, f("C821 to T"))
        testEqual(2, f("Arg76 to Trp"))
        testEqual(2, f("Arg149 to Gln"))
        testEqual(2, f("Pro274 to Leu"))
        testEqual(2, f("T320 to C"))
        testEqual(2, f("Leu107 to Pro"))
        testEqual(2, f("C631 to T"))
        testEqual(2, f("Arg211 to Cys"))
        testEqual(2, f("Ala215 to Thr"))
        testEqual(1, f("deletion of its cytoplasmic tail"))
        testEqual(1, f("nonsense mutation Q3X"))
        testEqual(0, f("R142Q"))
        testEqual(1, f("G-->A transition of a CpG dinucleotide"))
        testEqual(1, f("A C-->T transition of the same CpG"))
        testEqual(0, f("R142X"))
        testEqual(0, f("R142X"))
        testEqual(0, f("R142Q"))
        testEqual(1, f("replacement of this CpG hotspot by CpA"))
        testEqual(0, f("R142X"))
        testEqual(1, f("caused skipping of the exon"))
        testEqual(1, f("Absence of exon 5"))
        testEqual(0, f("Asp8Asn"))
        testEqual(1, f("G to A transition at nt22"))
        testEqual(1, f("asparagine for aspartic acid at codon 8"))
        testEqual(0, f("Asp8Asn"))
        testEqual(1, f("substitution of neutral asparagine for anionic aspartic acid"))
        testEqual(1, f("G to A transition is at a CpG dinucleotide"))
        testEqual(1, f("codon CAA encoding glutamine-2153 to UAA, a stop codon"))
        testEqual(1, f("attaching an epitope tag sequence to the C terminus of the editing protein"))
        testEqual(0, f("H15D"))
        testEqual(0, f("A83D"))
        testEqual(0, f("A179D"))
        testEqual(0, f("573 + IG-->A"))
        testEqual(0, f("H15D"))
        testEqual(0, f("A83D"))
        testEqual(0, f("A179D"))
        testEqual(1, f("skipping of exon 5"))
        testEqual(0, f("H15D"))
        testEqual(1, f("Replacement of these small hydrophobic Ala residues with the charged, more bulky Asp side chain"))
        testEqual(0, f("G20R"))
        testEqual(1, f("G to A transition at a CpG"))
        testEqual(1, f("glycine to arginine substitution at codon 20"))
        testEqual(0, f("26delA"))

        testEqual(0, f("delPhe1388"))
        testEqual(1, f("deleted C1 domain"))

        testEqual(0, f("Q115P"))
        testEqual(0, f("g.3912G>C"))
        testEqual(0, f("c.925delA"))
        testEqual(0, f("c.388+3insT"))

        testEqual(0, f("3992-9g-->a"))
        testEqual(2, f("3992-9g-->a mutation"))
        testEqual(2, f("G643 to A"))
        testEqual(2, f("leucine for arginine 90"))

        testEqual(1, f("deletion of aa 527-534"))
        testEqual(1, f("deletion of 10 and 8 residues from the N- and C-terminals"))
        testEqual(1, f("143 from alanine to glycine"))
        testEqual(1, f("alterations of amino acid residue 143 from alanine to glycine"))

        testEqual(1, f("trinucleotide deletion"))

        testEqual(1, f("arginine-141 to serine substitution"))
        testEqual(1, f("mutations at Arg885"))
        testEqual(1, f("point mutation at Cys93"))
        testEqual(1, f("heterozygous missense 3035G>T"))
        testEqual(2, f("synonymous 696T>C"))
        testEqual(2, f("missense Glu285Ala"))
        testEqual(1, f("somatic 16-bp deletion"))
        testEqual(1, f("serine 749 is phosphorylated"))
        testEqual(1, f("Ser58 to Glu substitution"))
        testEqual(1, f("deletion of"))
        testEqual(1, f("deletion of"))
        testEqual(1, f("deletion of"))
        testEqual(1, f("deletion of"))
        testEqual(0, f("GAT-->GTT, Asp-->Val"))
        testEqual(2, f("codon 98 GAT-->GTT, Asp-->Val"))
        testEqual(2, f("codon 92, TAC-->TAT"))
        testEqual(1, f("arginine-127 into glutamine and arginine-469 into tryptophan"))
        testEqual(2, f("arginine-127 into glutamine"))
        testEqual(2, f("arginine-469 into tryptophan"))

        # More difficult

        testEqual(2, f("chromothripsis"))
        testEqual(2, f("Morpholino knockdown"))
        testEqual(2, f("methionine replaces lysine 27"))
        testEqual(2, f("lysine(27)-to-methionine"))

        testEqual(1, f("C-tail displacement"))
        testEqual(1, f("22q11 deletion syndrome"))
        testEqual(1, f("hippocampal neuron L1 insertions"))
        testEqual(1, f("copy-number variants"))


class TestTmVarRegexNLDefiner(unittest.TestCase):
    def test_define(self):
        pass  # TODO


class TestTmVarNLDefiner(unittest.TestCase):
    def test_define(self):
        pass  # TODO

if __name__ == '__main__':
    unittest.main()

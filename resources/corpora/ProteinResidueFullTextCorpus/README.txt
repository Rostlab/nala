The contents of this downloaded tarball consist of a protein residue annotations of 50 full text articles This release consists only the annotations and not the articles itself. The Pubmed Identifier (PMID) of 50 full text articles is available in this package.

The corpus is available for download from: http://bionlp-corpora.sourceforge.net/proteinresidue/index.shtml

========
LICENSE
========
  Read License.txt before you utilize this corpus.

========
CONTENTS
========

1) The directory contains the following files:

     a) ProteinResidueFullText.tsv -> Protein-residue annotations of 50 full text articles.
     b) PMID.txt -> A list of the source PMIDs used as the basis of the full text articles annotated.


File format of the tsv file:
===========================

PMID	AnnotationType	Span_start	Span_End	AminoAcid_WildType_3_Letter_Abbrev	Residue_Position	AminoAcid_MutatedType_3_Letter_Abbrev	Residue_mention_in_original_text
10089511	Mutation	4	8	Glu	92	Lys	E92K
10366507	AminoAcidResidue	4	10	Lys	301		Lys301

The two valid Annotation Types are "Mutation" or "AminoAcidResidue". 
The AminoAcid_MutatedType_3_Letter_Abbrev column is empty or the string "NULL" in the case of an AminoAcidResidue.

Character Encoding
==================

UTF-8 encoding is used through-out the full text corpus, so please default to UTF-8 when using this corpus. 

e.g. In "Thr-459 → Ser" the unicode to match the "→" character is U+2192.

==========
Reference                               
==========

Please cite: 

Verspoor KM, Cohn JD, Ravikumar KE, Wall ME (Under Review) Text Mining Improves Prediction of Protein Functional Sites.

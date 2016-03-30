SNP Corpus Version 1.0 (as of March 17, 2011)
The corpus consists of 296 Medline citations. Citations were screened for mutations using a modified version of MutationFinder. The used regular expressions are available in 'mutationfinder.txt'. The SNPs (also missed by MutationFinder) were manually annotated with the corresponding dbSNP identifier, if available. Mutations without a valid dbSNP identifier were omitted. The corpus consists of 527 mutation rs-pairs. Due to licence restrictions of MEDLINE, abstracts are not contained in the corpus, but can be downloaded from MEDLINE using eUtils. To allow for a reproduction of our corpus, we also provide the original SNP mention in the abstract.

The corpus can be used to assess the performance of algorithms capable of associating variation mentions with dbSNP identifiers. It is published for academic use only and usage for development of commercial products is not permitted.

Please cite the following paper if you publish or present any research result obtained using this corpus:
@ARTICLE{Thomas2011,
    author = {Philippe E. Thomas and Roman Klinger and Laura I. Furlong and  Martin Hofmann-Apitius and Christoph M. Friedrich},
    title = {Challenges in the Association of Human Single Nucleotide Polymorphism Mentions with Unique Database Identifiers},
    journal = {submitted},
    year = {2011}    
}

The corpus copromises the following files:

annotations.txt       	  	Annotations for the corpus
guideline.pdf			Annotation guidelines for annotation
LICENSE  			General license information for this corpus
mutationfinder-license.txt  	Specific license information for MutationFinder
README.txt			This readme

The annotations.txt compromises the following columns:
PMID:		Pubmed identifier.
Entity:		Original string in the text.
SNP:		String describing the extracted mutation in the following format: <Wildtype><Position><Mutated>. This string may deviate from the actual string in the abstract and is not normalized for nomenclature mentions.
Start:		Start position of the mutation descriptor in the abstract
End:		End position of the mutation descriptor in the abstract
rs:		dbSNP identifier for the current SNP. The dbSNP-identifier has been extracted from the text and manually associated with the SNP.
type:		Describes the type of SNP; here Protein Sequence Mutation (PSM) or Nucleotide Sequence Mutation (NSM)

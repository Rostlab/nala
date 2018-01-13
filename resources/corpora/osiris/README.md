========================================================================================== 
OSIRIS corpus version 0.2                                                              
Contact: Laura Ines Furlong <lfurlong@imim.es>                                             
========================================================================================== 

If you use this corpus to produce results for publication, please cite us:

Furlong LI, Dach H, Hofmann-Apitius M, Sanz F.OSIRISv1.2: a named entity recognition system for sequence variants of genes in biomedical literature. BMC Bioinformatics 2008, 9:84.


About the files:

Files  articlexx.txt: contain the PMID, title and abstract of each MEDLINE abstract

File   articlexx.txt.ann: contain the annotation of variation and gene mentions for each MEDLINE abstract

The file numbers span from 1 to 105 (there are 105 abstracts in the OSIRIS corpus).


About the annotation tags:

For the variation
	-so: state original
	-lo: location
	-sa: state altered
	-ty: variation type

For the gene
	-ge: gene

The comment tag is used to specify the dbSNP identifier of each variation
entity.

-------

Otherwise you can use the OSIRIScorpusv01 (.xml and .dtd) in format of one XML-file.

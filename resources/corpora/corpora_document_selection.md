# Corpora document selection approaches


## SETH

mostly SNPs


## tmVar
Diseases Category[Mesh] AND (mutation[MeSH Terms] OR polymorphism, genetic[MeSH Terms]) AND humans[MeSH Terms]

Full:

Diseases Category[Mesh] AND (mutation[MeSH Terms] OR polymorphism, genetic[MeSH Terms]) AND (DNA[Title/Abstract] OR nucleotide[Title/Abstract]) AND (deletion[Title/Abstract] OR substitution[Title/Abstract] OR insertion[Title/Abstract] OR duplication[Title/Abstract] OR indel[Title/Abstract] OR delin[Title/Abstract] OR conversion[Title/Abstract] OR translocation[Title/Abstract] OR inversion[Title/Abstract]) AND (codon[Title/Abstract] OR exon[Title/Abstract] OR intron[Title/Abstract] OR allele[Title/Abstract] OR gene[Title/Abstract] OR sequence[Title/Abstract]) AND (genotyp*[Title/Abstract] OR homozyg*[Title/Abstract] OR heterozyg*[Title/Abstract]) AND hasabstract[text] AND humans[MeSH Terms] AND English[lang] NOT Review[ptyp]


## Variome
search query consisting of the three most common Lynch syndrome genes: ‘MLH1 or MSH2 or MSH6’


## IDP4 and nala

SWIS-PROT, listed for `variation` or `mutagenesis`


## nala_random

mutation AND ("Science"[Journal] OR Cell[Journal] OR Nature[Journal]) AND ("2013"[Date - Publication] : "2016/01/01"[Date - Publication]) AND hasabstract[text] AND Diseases Category[Mesh] AND (mutation[MeSH Terms] OR polymorphism, genetic[MeSH Terms])

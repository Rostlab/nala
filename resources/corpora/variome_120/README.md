Copied from: https://bitbucket.org/readbiomed/mutationtoolcomparison/src/84bd508bea8f/data/Variome_corpus/?at=default

Note: the number of annotations in the folder `annotations_dna_mutations_explicit` + `annotations_protein_mutations_explicit` does make 118 annotations. This number coincides with the description in the paper [Jimeno and Verspor 2014](http://www.ncbi.nlm.nih.gov/pubmed/25285203.2). A private email conversation with Antonio Jimeno revealed:

> As you have realized, from the Variome Corpus, we selected the
> mutations that could be mapped to a change in genes or proteins. In
> the repository there are three folders, one for mutations in general
> and one for protein mutations and another one for DNA mutations. The
> generic one has 120, while if you add the other two folders you get
> 118. The generic was developed first as a filter to the Variome Corpus
> mutations to contain only the ones specifying a change in a sequence.
> Then, we further split this list into DNA and protein mutations. The
> two mutation mentions that you show below did not fit into any of the
> two categories exactly and were left out. I am wondering if this might
> be a problem for your experiments.

We reasoned that we could use the whole 120 set. Juan Miguel's answer (in Spanish):

> Más bien parece que las 2 anotaciones extra son en realidad 2 mutaciones cada una (DNA + protein). Creo que utilizaremos el set de 120. Después de todo son 2 buenos ejemplos de mutaciones escritas en lenguaje natural que es precisamente lo que queremos mejorar.

We also note that the 2 extra annotations overlap:

(`1334229-04-Results-p01.ann`)

> T59	mutation 477 558	codons 37 and 45, all were C→T transitions, leading to Ser→Phe amino acid changes
> T87_merge_merge	mutation 371 507	loss of one of the Ser/Thr phosphorylation sites and subsequent stabilisation of the protein, occurred at codons 37 and 45, all were C→T

But two other annotations in "Var118" overlap too:

(`2386495-04-Results-p02.ann`)

> T1	mutation 374 385	1825del3595
> T34_merge	mutation 359 385	c.423-1662_531+1825del3595

These 2 overlapping cases will affect exact performance but not overlapping. So we leave as they are.

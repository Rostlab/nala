The folder contains the methods' predictions on the considered corpora.

The structure is as follows: `method_name/tested_corpus/`

The predictions are written in an arbitrary format, whatever it was easiest to get from the corresponding method.
Furthermore, each `tested_corpus` folder contains the file `results.tsv` that summarizes the performance results.


Some example predictions of other methods needed for the nala paper (Table 1) were run as follows:

* MutationFinder: used original python (2) code: http://mutationfinder.sourceforge.net
* SETH: used our fork of SETH: https://github.com/juanmirocks/SETH
* tmVar: used the web demo: https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/tmTools/demo/tmVar/

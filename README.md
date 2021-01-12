# ☝️ We moved

This library is not maintained anymore.

We moved nala to [the text annotation tool, tagtog](https://www.tagtog.net):

[![tagtog, The Text Annotation Tool to Train AI](http://docs.tagtog.net/assets/img/circle_2leafstext.png)](https://www.tagtog.net)

---
---
---

[![Build Status](https://travis-ci.org/Rostlab/nala.svg?branch=develop)](https://travis-ci.org/Rostlab/nala)
[![codecov](https://codecov.io/gh/Rostlab/nala/branch/develop/graph/badge.svg)](https://codecov.io/gh/Rostlab/nala)


## nala

_Text mining_ method for the extraction of _sequence variants_ (genes or proteins) written in standard (ST) format (e.g. "E6V") or complex **natural language** (NL) (e.g. "glutamic acid was substituted by valine at residue 6").

Publication: [Cejuela et al., nala: text mining natural language mutation mentions, Bioinformatics, 2018](https://academic.oup.com/bioinformatics/article/33/12/1852/2991428)


## Install

Requires Python 3.6


### From source

```shell
git clone https://github.com/Rostlab/nala.git
cd nala
poetry shell
poetry install
python3 -m nalaf.download_data
```

NOTE: if you prefer installing with `pip` (instead of `poetry`), you will need pip >= 19.0, and then do:

```shell
pip install -r requirements.txt
pip install .
```


## Developing

### Test

If you want to run the unit tests (excluding the slow ones) do:

```shell
nosetests -a '!slow'
```

### Troubleshooting on Windows

The module `python-crfsuite` (`pycrfsuite`) may not install on Windows. See the [original module](https://github.com/tpeng/python-crfsuite).


### Run Examples

* Simple:
  * `python3 nala.py -p 15878741 12625412 # i.e. list of PMIDs to tag`
  * `python3 nala.py -s "Standard (ST) examples: Asp8Asn or delPhe1388. Semi-standard (SST) examples: 3992-9g-->a mutation. Natural language (NL) examples: glycine was substituted by lysine at residue 18 (Gly18Lys)"`

* Programmatic access: [nala/learning/train.py](nala/learning/train.py)

* API annotation service via tagtog.net: https://www.tagtog.net/-corpora/IDP4+

[![Build Status](https://travis-ci.org/Rostlab/nala.svg?branch=develop)](https://travis-ci.org/Rostlab/nala)
[![codecov](https://codecov.io/gh/Rostlab/nala/branch/develop/graph/badge.svg)](https://codecov.io/gh/Rostlab/nala)


# nala

_Text mining_ method for the extraction of _sequence variants_ (genes or proteins) written in standard (ST) format (e.g. "E6V") or complex natural language (NL) (e.g. "glutamic acid was substituted by valine at residue 6").

Motivation: _pending submitted paper_ (soon to be updated)


# Install

##  Requirements

* Requires Python 3 (>= 3.4)
* [nalaf](https://github.com/Rostlab/nalaf)
  * [unmanaged dependencies by nalaf, see comments in `setup.py`](https://github.com/Rostlab/nalaf/blob/develop/setup.py)

## Install Code

```shell
git clone https://github.com/Rostlab/nala.git
cd nala
python3 setup.py install
python3 -m nalaf.download_corpora
```

 If you want to run the unit tests (excluding the slow ones) do:

```shell
python3 setup.py nosetests -a '!slow'
```

 Note: When we eventually register the package on pypi, the first 3 steps will be replaced with just this next one:

```shell
pip3 install nala
```

### Troubleshooting on Windows

The module `python-crfsuite` (`pycrfsuite`) may not install on Windows. See the [original module](https://github.com/tpeng/python-crfsuite).

# Examples

* Simple:
  * `python3 nala.py -p 15878741 12625412 # i.e. list of PMIDs to tag`
 * `python3 nala.py -s "Standard (ST) examples: Asp8Asn or delPhe1388. Semi-standard (SST) examples: 3992-9g-->a mutation. Natural language (NL) examples: glycine was substituted by lysine at residue 18 (Gly18Lys)"`

* Full control: [nala/learning/train.py](nala/learning/train.py)

* API access: https://www.tagtog.net/-corpora/IDP4+

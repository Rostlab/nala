[![Build Status](https://travis-ci.com/Rostlab/nala.svg?token=VhCZKjoiPjzKEaXybidS)](https://travis-ci.com/Rostlab/nala)

# nala

_Text mining_ method for the extraction of _sequence variants_ (genes or proteins) written in standard (ST) format (e.g. "E6V") or complex natural language (NL) (e.g. "glutamic acid was substituted by valine at residue 6").

Motivation: _pending submitted paper_ (soon to be updated)


# Install

##  Requirements

* Requires Python 3 (>= 3.3)
* [nalaf](https://github.com/Rostlab/nalaf)

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

Run:

* `python3 nala.py -p 15878741 12625412`
* `python3 nala.py -s "This are examples: Asp8Asn or delPhe1388 (ST); 3992-9g-->a mutation (SST); glycine was substituted by lysine at residue 18 (NNL)"`

For API access, see: https://www.tagtog.net/-corpora/IDP4+

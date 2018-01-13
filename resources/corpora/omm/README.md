
* [OpenMutationMiner (OMM) Software](http://www.semanticsoftware.info/open-mutation-miner)
* [First Release of OMM](http://www.semanticsoftware.info/first-open-mutation-miner-release)
* [Original Paper (full-text)](http://bmcgenomics.biomedcentral.com/articles/10.1186/1471-2164-13-S4-S10)

#### Mutation series detection corpus

We prepared a corpus containing 11 full-text PubMed articles on enzymes to assess the efficiency of the system in detecting mutation series. We ensured that all these documents contain multiple mutation mentions. These documents contain a total of 1306 mutations and 271 mutation series. The list of documents used for evaluation is provided in an additional file [see Additional file 1].

#### Impact extraction corpora

We selected 40 PubMed IDs and manually annotated them with the impact information. For each impact mention, only the part of the sentence mentioning the mutation and the impact was selected. Thus, if a sentence expresses multiple impacts, all are annotated separately [see Additional file 2 for manual annotations]. The impacts are grounded to the respective mutations and the EC number of experimented enzymes is specified. The list of documents used for evaluation is provided in an additional file [see Additional file 1].


#### Files in folder

* PDF with list of documents for 2 separate corpora "12864_2012_4031_MOESM1_ESM.pdf"
* Manual annotations (annotated corpus) "12864_2012_4031_MOESM2_ESM.txt"
* OMM predictions (predicted corpus) "12864_2012_4031_MOESM3_ESM.txt"

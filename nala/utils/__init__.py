"""
nala.utils contains classes that help for instance with downloading doc- uments from the internet.
The import and export classes are contained there as well. Other classes are:
– Cacheprovidingcachingforclassesthatneedtodownloadstaticcontent often.
– GNormPlus which annotates either full-text documents or PubMed abstracts through the RESTApi from PubTator.
– Tagger which implements an easy interface to be able to use external taggers for example TmVarTagger, that can use PubTator as well, to download mutation mentions through the tmVar method.
– Uniprot helps with normalising EntrezGene IDs [22] to Uniprot IDs [23]. This is part of the normalisation process in class GNormPlusGeneTagger.
"""
PRO_CLASS_ID = 'e_1'
MUT_CLASS_ID = 'e_2'
ORG_CLASS_ID = 'e_3'
PRO_REL_MUT_CLASS_ID = 'r_4'  # e_1/e_2
PRO_REL_ORG_CLASS_ID = 'r_5'  # e_1/e_3
THRESHOLD_VALUE = 1
ENTREZ_GENE_ID = 'n_4'
UNIPROT_ID = 'n_5'


def get_prepare_pipeline_for_best_model():
    """
    Helper method that returns an instance of PrepareDatasetPipeline
    which uses the best configuration for predicating mutation mentions.

    :returns nalaf.structures.dataset_pipelines.PrepareDatasetPipeline
    """
    from nalaf.structures.dataset_pipelines import PrepareDatasetPipeline
    from nalaf.features.simple import SimpleFeatureGenerator, SentenceMarkerFeatureGenerator
    from nalaf.features.stemming import PorterStemFeatureGenerator
    from nalaf.features.window import WindowFeatureGenerator
    from nala.features.tmvar import TmVarFeatureGenerator, TmVarDictionaryFeatureGenerator

    include = ['pattern0[0]', 'pattern1[0]', 'pattern2[0]', 'pattern3[0]', 'pattern4[0]', 'pattern5[0]',
               'pattern6[0]', 'pattern7[0]', 'pattern8[0]', 'pattern9[0]', 'pattern10[0]', 'word[0]', 'stem[0]']
    return PrepareDatasetPipeline(feature_generators=[SimpleFeatureGenerator(), PorterStemFeatureGenerator(),
                                                      SentenceMarkerFeatureGenerator(),
                                                      TmVarFeatureGenerator(), TmVarDictionaryFeatureGenerator(),
                                                      WindowFeatureGenerator(template=(-3, -2, -1, 1, 2, 3),
                                                                             include_list=include)])


def get_word_embeddings_feature_generator():
    """
    :returns: nalaf.features.embeddings.WordEmbeddingsFeatureGenerator
    """
    import os
    import tarfile

    import pkg_resources
    import requests
    from nalaf.features.embeddings import WordEmbeddingsFeatureGenerator
    from nalaf import print_verbose

    we_model = pkg_resources.resource_filename('nala.data', os.path.join('model', 'model'))
    if not os.path.exists(we_model):
        answer = input('Word Embeddings model is missing. Do you want us to download it? [y/n]')

        # Download the model
        if answer.lower() == 'y':
            print_verbose('Downloading')
            model_url = 'https://rostlab.org/~cejuela/model.tar.gz'
            we_model_tar_gz = pkg_resources.resource_filename('nala.data', 'we_model.tar.gz')

            response = requests.get(url=model_url, stream=True)
            with open(we_model_tar_gz, 'wb') as file:
                for chunk in response.iter_content(8048):
                    if chunk:
                        file.write(chunk)
            # Unpack the model
            print_verbose('Extracting')

            tar = tarfile.open(we_model_tar_gz)
            tar.extractall(path=pkg_resources.resource_filename('nala.data', ''))
            tar.close()
        else:
            return None

    return WordEmbeddingsFeatureGenerator(we_model)

"""
nala.utils contains classes that help for instance with downloading doc- uments from the internet.

The import and export classes are contained there as well. Other classes are:
– Cacheprovidingcachingforclassesthatneedtodownloadstaticcontent often.
– GNormPlus which annotates either full-text documents or PubMed abstracts through the RESTApi from PubTator.
– Tagger which implements an easy interface to be able to use external taggers for example TmVarTagger, that can use PubTator as well, to download mutation mentions through the tmVar method.
– Uniprot helps with normalising EntrezGene IDs [22] to Uniprot IDs [23]. This is part of the normalisation process in class GNormPlusGeneTagger.
"""

import os
from nalaf.structures.dataset_pipelines import PrepareDatasetPipeline
from nalaf.features.simple import SentenceMarkerFeatureGenerator
from nalaf.features.stemming import SpacyLemmatizer
from nalaf.features.parsing import SpacyPosTagger
from nalaf.features.window import WindowFeatureGenerator
from nala.features.tmvar import TmVarFeatureGenerator, TmVarDictionaryFeatureGenerator
from nala.features.nl_mutations import NLMentionFeatureGenerator
from nalaf.preprocessing.tokenizers import TmVarTokenizer

PRO_CLASS_ID = 'e_1'
MUT_CLASS_ID = 'e_2'
ORG_CLASS_ID = 'e_3'
PRO_REL_MUT_CLASS_ID = 'r_4'  # e_1/e_2
PRO_REL_ORG_CLASS_ID = 'r_5'  # e_1/e_3
THRESHOLD_VALUE = 1

__nala_repo_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def nala_repo_path(listOrString):
    if type(listOrString) is str:
        return os.path.join(__nala_repo_root, listOrString)
    else:
        return os.path.join(__nala_repo_root, *listOrString)


def get_prepare_pipeline_for_best_model(use_windows=True, we_params=None, nl_features=None):
    """
    Helper method that returns an instance of PrepareDatasetPipeline
    which uses the best configuration for predicating mutation mentions.
    if we_params is empty dict, no we is applied

    :returns nalaf.structures.dataset_pipelines.PrepareDatasetPipeline
    """

    default_we_params = {'additive': None, 'multiplicative': None, 'location': None}
    we_params = default_we_params if we_params is None else we_params

    generators = [
        SpacyLemmatizer(),
        SentenceMarkerFeatureGenerator(),
        TmVarFeatureGenerator(get_mutation_features=True),
        TmVarDictionaryFeatureGenerator(),
    ]

    include = []

    if nl_features:
        f = NLMentionFeatureGenerator(nl_features['threshold'])
        if nl_features['window']:
            include.extend(['tag_dict[0]', 'nl_tag_dict[0]'])

        generators.append(f)

    if use_windows:
        include.extend(['pattern0[0]', 'pattern1[0]', 'pattern2[0]', 'pattern3[0]', 'pattern4[0]', 'pattern5[0]',
                        'pattern6[0]', 'pattern7[0]', 'pattern8[0]', 'pattern9[0]', 'pattern10[0]', 'stem[0]'])
        f = WindowFeatureGenerator(template=(-4, -3, -2, -1, 1, 2, 3, 4), include_list=include)
        generators.append(f)

    if we_params:
        generators.append(get_word_embeddings_feature_generator(we_params['location'], we_params['additive'], we_params['multiplicative']))

    return PrepareDatasetPipeline(feature_generators=generators)


def get_prepare_pipeline_for_best_model_general(use_windows=True, we_params=None, nl_features=None):
    """
    Helper method that returns an instance of PrepareDatasetPipeline
    which uses the best configuration for predicating any-domain mentions.

    if we_params is empty dict, no we is applied

    :returns nalaf.structures.dataset_pipelines.PrepareDatasetPipeline
    """

    # MAYBE ml-performance: use more general-domain tokenizer such as NLTK's
    tokenizer = TmVarTokenizer()

    default_we_params = {'additive': None, 'multiplicative': None, 'location': None}
    we_params = default_we_params if we_params is None else we_params

    generators = [
        SpacyLemmatizer(),
        SpacyPosTagger(),
        SentenceMarkerFeatureGenerator(),
        TmVarFeatureGenerator(get_mutation_features=False)
    ]

    windows_include = []

    if nl_features:
        f = NLMentionFeatureGenerator(nl_features['threshold'])
        if nl_features['window']:
            windows_include.extend(['tag_dict[0]', 'nl_tag_dict[0]'])

        generators.append(f)

    if use_windows:
        windows_include.extend(['stem[0]', 'pos[0]'])
        f = WindowFeatureGenerator(template=(-2, -1, 1, 2), include_list=windows_include)
        generators.append(f)

    if we_params:
        generators.append(get_word_embeddings_feature_generator(we_params['location'], we_params['additive'], we_params['multiplicative']))

    return PrepareDatasetPipeline(tokenizer=tokenizer, feature_generators=generators)


_SINGLETON_WE_GENERATOR = None


def get_word_embeddings_feature_generator(model_location=None, additive=None, multiplicative=None):
    """
    :returns: nalaf.features.embeddings.WordEmbeddingsFeatureGenerator
    """
    global _SINGLETON_WE_GENERATOR

    if _SINGLETON_WE_GENERATOR is None:
        additive = 0 if additive is None else additive
        multiplicative = 1 if multiplicative is None else multiplicative

        import tarfile

        import pkg_resources
        import requests
        from nalaf.features.embeddings import WordEmbeddingsFeatureGenerator
        from nalaf import print_verbose, print_warning

        if model_location is None:
            # D=100, no discretization, epoch=1, window=10
            last_model = "word_embeddings_2016-03-28"
            we_model = pkg_resources.resource_filename('nala.data', os.path.join(last_model, 'word_embeddings.model'))
            if not os.path.exists(we_model):
                print_warning('Downloading Word Embeddings Model (this may take a long time). Expected path: ' + we_model)
                # TODO requests doesn't support ftp, but better use: ftp://rostlab.org/jmcejuela/...last_model...
                tar = '{}.tar.gz'.format(last_model)
                model_url = '{}/{}'.format('https://rostlab.org/~cejuela', tar)
                we_model_tar_gz = pkg_resources.resource_filename('nala.data', tar)

                response = requests.get(url=model_url, stream=True)
                with open(we_model_tar_gz, 'wb') as file:
                    for chunk in response.iter_content(8048):
                        if chunk:
                            print('.', end="", flush=True)
                            file.write(chunk)
                    print()
                # Unpack the model
                print_verbose('Extracting')

                tar = tarfile.open(we_model_tar_gz)
                tar.extractall(path=pkg_resources.resource_filename('nala.data', ''))
                tar.close()
            _SINGLETON_WE_GENERATOR = WordEmbeddingsFeatureGenerator(we_model, additive, multiplicative)
        else:
            _SINGLETON_WE_GENERATOR = WordEmbeddingsFeatureGenerator(model_location, additive, multiplicative)

    return _SINGLETON_WE_GENERATOR

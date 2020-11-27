from setuptools import setup
from setuptools import find_packages


def readme():
    with open('README.md') as file:
        return file.read()


setup(
    name='nala',
    version='0.3.8-SNAPSHOT',
    description='Pipeline for NER of natural language mutation mentions',
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic'
    ],
    keywords='crf mutation natural language ner',
    url='https://github.com/Rostlab/nala',
    author='Aleksandar Bojchevski, Carsten Uhlig, Juan Miguel Cejuela',
    author_email='nala@rostlab.org',
    # license='UNKNOWN',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        # 'nalaf == 0.5.11' -- Dependencies are declared in the Pipfile
    ],
    # dependency_links=[
    #    'git+ssh://git@github.com/Rostlab/nalaf/tree/develop#egg=nalaf'
    # ],
    include_package_data=True,
    zip_safe=False
)

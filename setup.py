from setuptools import setup
from setuptools import find_packages


def readme():
    with open('README.md') as file:
        return file.read()


setup(
    name='nala',
    version='0.2.1-SNAPSHOT',
    description='Pipeline for NER of natural language mutation mentions',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing :: Linguistic'
    ],
    keywords='crf mutation natural language ner',
    url='https://github.com/Rostlab/nala',
    author='Aleksandar Bojchevski, Carsten Uhlig, Juan Miguel Cejuela',
    author_email='nala@rostlab.org',
    # license='UNKNOWN',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'nalaf == 0.3.2'
    ],
    # dependency_links=[
    #    'git+ssh://git@github.com/Rostlab/nalaf/tree/develop#egg=nalaf'
    # ],
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    setup_requires=['nose>=1.0'],
)

from setuptools import setup
from setuptools import find_packages


def readme():
    with open('README.md') as file:
        return file.read()

setup(
    name='nala',
    version='0.1.1',
    description='Pipeline for NER of natural language mutation mentions',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing :: Linguistic'
    ],
    keywords='crf mutation natural language ner',
    url='https://github.com/carstenuhlig/thesis-alex-carsten',
    author='Aleksandar Bojchevski, Carsten Uhlig',
    author_email='email@somedomain.com',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'nalaf'
    ],
    #dependency_links=[
    #    'git+ssh://git@github.com/Rostlab/nalaf/tree/develop#egg=nalaf'
    #],
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    setup_requires=['nose>=1.0'],
)

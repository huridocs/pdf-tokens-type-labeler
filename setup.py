import setuptools
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

PROJECT_NAME = 'pdf-tokens-type-labeler'

setup(
    name=PROJECT_NAME,
    packages=setuptools.find_packages(),
    package_dir={PROJECT_NAME: 'src'},
    version='0.4',
    url='https://github.com/huridocs/pdf-tokens-type-labeler',
    author='HURIDOCS',
    description='This tool returns each token type inside a PDF',
    install_requires=requirements
)

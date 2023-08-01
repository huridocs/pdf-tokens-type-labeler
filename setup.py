import setuptools
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='pdf-tokens-type-labeler',
    version='0.1',
    packages=setuptools.find_packages(),
    url='https://github.com/huridocs/pdf-tokens-type-labeler',
    author='HURIDOCS',
    description='This tool returns each token type inside a PDF',
    install_requires=requirements
)

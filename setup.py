from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

PROJECT_NAME = 'pdf-tokens-type-labeler'

setup(
    name=PROJECT_NAME,
    packages=[PROJECT_NAME],
    package_dir={PROJECT_NAME: 'src', 'pdf_features': 'src/pdf_features'},
    version='0.5',
    url='https://github.com/huridocs/pdf-tokens-type-labeler',
    author='HURIDOCS',
    description='This tool returns each token type inside a PDF',
    install_requires=requirements
)


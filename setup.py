from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

PROJECT_NAME = "pdf-tokens-type-labeler"

setup(
    name=PROJECT_NAME,
    packages=["pdf_tokens_type_trainer", "pdf_features", "pdf_token_type_labels"],
    package_dir={"": "src"},
    version="0.16",
    url="https://github.com/huridocs/pdf-tokens-type-labeler",
    author="HURIDOCS",
    description="This tool returns each token type inside a PDF",
    install_requires=requirements,
)

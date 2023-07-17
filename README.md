<h3 align="center">PDF tokens type labeler</h3>
<p align="center">This tool returns each token type inside a PDF</p>

## Tokens Types List


* FORMULA
* FOOTNOTE
* LIST
* TABLE
* FIGURE
* TITLE
* TEXT

## Quick Start
Create venv:

    make install_venv

Get the token types from a PDF:

    source venv/bin/activate
    python src/predict.py /path/to/pdf


## Train a new model
Create venv:

    make install_venv

Get the token types from a PDF:

    source venv/bin/activate
    python src/train.py

## Use a custom model
    
    python src/predict.py /path/to/pdf --model-path /path/to/model
    
<h3 align="center">PDF tokens type labeler</h3>
<p align="center">This tools process PDFs and returns the tokens type</p>

## Tokens Types List


* FORMULA
* FOOTNOTE
* LIST
* TABLE
* FIGURE
* TITLE
* TEXT

---

This service provides one endpoint to get paragraphs from PDFs. The paragraphs
contain the page number, the position in the page, the size, and the text. Furthermore, there is 
an option to get an asynchronous flow using message queues on redis.

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
    
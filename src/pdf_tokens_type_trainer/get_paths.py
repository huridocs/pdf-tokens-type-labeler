from os.path import join
from pathlib import Path


def get_token_type_labeled_data_path(pdf_labeled_data_project_path: str):
    return Path(join(pdf_labeled_data_project_path, "labeled_data", "token_type"))


def get_paragraph_extraction_labeled_data_path(pdf_labeled_data_project_path: str):
    return Path(join(pdf_labeled_data_project_path, "labeled_data", "paragraph_extraction"))


def get_xml_path(pdf_labeled_data_project_path: str):
    return Path(join(pdf_labeled_data_project_path, "pdfs"))

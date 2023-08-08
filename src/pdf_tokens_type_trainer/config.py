from os.path import join
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.absolute()

LABELED_DATA_ROOT_PATH = join(ROOT_PATH.parent.parent, "pdf-labeled-data")
TRAINED_MODEL_PATH = join(ROOT_PATH.parent, "model", "pdf_tokens_type.model")

TOKEN_TYPE_LABELED_DATA_PATH = join(LABELED_DATA_ROOT_PATH, "labeled_data", "token_type")
PARAGRAPH_EXTRACTION_LABELED_DATA_PATH = join(LABELED_DATA_ROOT_PATH, "labeled_data", "paragraph_extraction")
XML_PATHS = join(LABELED_DATA_ROOT_PATH, "pdfs")

XML_NAME = "etree.xml"
LABELS_FILE_NAME = "labels.json"

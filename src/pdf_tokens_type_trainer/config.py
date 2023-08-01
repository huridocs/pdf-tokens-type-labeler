from os.path import join
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.absolute()

LABELED_DATA_ROOT_PATH = ROOT_PATH.parent.parent
TRAINED_MODEL_PATH = join(ROOT_PATH.parent, "model", "pdf_tokens_type.model")

LABELED_DATA_PATH = join(LABELED_DATA_ROOT_PATH, "pdf-labeled-data", "labeled_data", "token_type")
LABELED_XML_PATH = join(LABELED_DATA_ROOT_PATH, "pdf-labeled-data", "pdfs")

XML_NAME = "etree.xml"
LABELS_FILE_NAME = "labels.json"

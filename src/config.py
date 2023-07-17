from os.path import join
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.absolute()

HUGGINGFACE_PATH = join(ROOT_PATH, "huggingface")
LABELED_DATA_BASE_PATH = join(ROOT_PATH, "labeled_data")

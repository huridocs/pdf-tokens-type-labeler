from os import listdir
from os.path import join
from pathlib import Path

from ModelConfiguration import ModelConfiguration
from Trainer import Trainer
from config import LABELED_DATA_BASE_PATH
from pdf_features.PdfFeatures import PdfFeatures


def load_labeled_data():
    pdf_features: list[PdfFeatures] = list()
    for labeled_data_folder_name in listdir(LABELED_DATA_BASE_PATH):
        if "train" not in labeled_data_folder_name:
            continue

        labeled_data_path = join(LABELED_DATA_BASE_PATH, labeled_data_folder_name)
        files_paths = [join(labeled_data_path, file_name) for file_name in listdir(labeled_data_path)]

        print(f"loading {labeled_data_folder_name} from {labeled_data_path}")
        pdf_features.extend([PdfFeatures.from_poppler_etree(file_path) for file_path in files_paths])

    return pdf_features


def train():
    model_path = join(Path(__file__).parent.parent, "model", "pdf_tokens_type.model")
    Path(model_path).parent.mkdir(exist_ok=True)
    pdf_features = load_labeled_data()
    model_configuration = ModelConfiguration()
    trainer = Trainer(pdf_features, model_configuration)
    trainer.train(model_path)


if __name__ == "__main__":
    train()

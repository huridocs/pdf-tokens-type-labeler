from os import listdir
from os.path import join

from config import LABELED_DATA_BASE_PATH
from pdf_features.PdfFeatures import PdfFeatures


def load_labeled_data(filter_in: str = None):
    if filter_in:
        print(f"Loading only datasets with the key word: {filter_in}")

    pdf_features: list[PdfFeatures] = list()
    for labeled_data_folder_name in listdir(LABELED_DATA_BASE_PATH):
        if filter_in and filter_in not in labeled_data_folder_name:
            continue

        labeled_data_path = join(LABELED_DATA_BASE_PATH, labeled_data_folder_name)
        files_paths = [join(labeled_data_path, file_name) for file_name in listdir(labeled_data_path)]

        print(f"loading {labeled_data_folder_name} from {labeled_data_path}")
        pdf_features.extend([PdfFeatures.from_poppler_etree(file_path) for file_path in files_paths])

    return pdf_features

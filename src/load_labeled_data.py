import os
from os import listdir
from os.path import join, isdir

from config import LABELED_DATA_PATH
from pdf_features.PdfFeatures import PdfFeatures


def load_labeled_data(filter_in: str = None):
    if filter_in:
        print(f"Loading only datasets with the key word: {filter_in}")
        print()

    pdf_features: list[PdfFeatures] = list()
    for dataset_name in listdir(LABELED_DATA_PATH):
        if filter_in and filter_in not in dataset_name:
            continue

        dataset_path = join(LABELED_DATA_PATH, dataset_name)

        if not isdir(dataset_path):
            continue

        dataset_pdf_name = [(dataset_name, pdf_name) for pdf_name in listdir(dataset_path)]

        print(f"loading {dataset_name} from {dataset_path}")
        pdf_features.extend([PdfFeatures.from_labeled_data(dataset, pdf_name) for dataset, pdf_name in dataset_pdf_name])

    return pdf_features

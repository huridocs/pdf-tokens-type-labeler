from os import listdir
from os.path import join, isdir

from pdf_features.PdfFeatures import PdfFeatures
from pdf_tokens_type_trainer.get_paths import get_token_type_labeled_data_path


def loop_datasets(pdf_labeled_data_project_path: str, filter_in: str):
    type_labeled_data_path = get_token_type_labeled_data_path(pdf_labeled_data_project_path)
    for dataset_name in listdir(type_labeled_data_path):
        if filter_in and filter_in not in dataset_name:
            continue

        dataset_path = join(type_labeled_data_path, dataset_name)

        if not isdir(dataset_path):
            continue

        yield dataset_name, dataset_path


def load_labeled_data(pdf_labeled_data_project_path: str, filter_in: str = None):
    if filter_in:
        print(f"Loading only datasets with the key word: {filter_in}")
        print()

    pdfs_features: list[PdfFeatures] = list()

    for dataset_name, dataset_path in loop_datasets(pdf_labeled_data_project_path, filter_in):
        print(f"loading {dataset_name} from {dataset_path}")

        dataset_pdf_name = [(dataset_name, pdf_name) for pdf_name in listdir(dataset_path)]
        for dataset, pdf_name in dataset_pdf_name:
            pdf_features = PdfFeatures.from_labeled_data(pdf_labeled_data_project_path, dataset, pdf_name)
            pdfs_features.append(pdf_features)

    return pdfs_features

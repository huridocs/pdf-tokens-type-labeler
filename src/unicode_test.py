import unicodedata

from tqdm import tqdm

from pdf_features.PdfFeatures import PdfFeatures
from pdf_token_type_labels.load_labeled_data import load_labeled_data
from pdf_tokens_type_trainer.config import PDF_LABELED_DATA_ROOT_PATH

if __name__ == '__main__':
    pdfs_features: list[PdfFeatures] = load_labeled_data(PDF_LABELED_DATA_ROOT_PATH, filter_in="test")

    categories = set()
    for pdf_features in tqdm(pdfs_features):
        for page, token in pdf_features.loop_tokens():
            for letter in token.content:
                categories.add(unicodedata.category(letter))
                
    print(categories)
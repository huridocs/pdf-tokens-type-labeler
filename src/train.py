from os.path import join
from pathlib import Path


from pdf_token_type_labels.load_labeled_data import load_labeled_data
from pdf_tokens_type_trainer.ModelConfiguration import ModelConfiguration
from pdf_tokens_type_trainer.TokenTypeTrainer import TokenTypeTrainer
from pdf_tokens_type_trainer.config import TRAINED_MODEL_PATH, PDF_TOKENS_TYPE_ROOT_PATH, PDF_LABELED_DATA_ROOT_PATH


def train(filter_in: str = None):
    Path(join(PDF_TOKENS_TYPE_ROOT_PATH, TRAINED_MODEL_PATH)).parent.mkdir(exist_ok=True)
    pdf_features = load_labeled_data(PDF_LABELED_DATA_ROOT_PATH, filter_in)
    model_configuration = ModelConfiguration()
    trainer = TokenTypeTrainer(pdf_features, model_configuration)
    trainer.train(TRAINED_MODEL_PATH)


if __name__ == "__main__":
    train()

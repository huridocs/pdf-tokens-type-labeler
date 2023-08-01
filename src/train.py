from pathlib import Path


from load_labeled_data import load_labeled_data
from pdf_tokens_type_trainer.ModelConfiguration import ModelConfiguration
from pdf_tokens_type_trainer.Trainer import Trainer
from pdf_tokens_type_trainer.config import TRAINED_MODEL_PATH


def train(filter_in: str = None):
    Path(TRAINED_MODEL_PATH).parent.mkdir(exist_ok=True)
    pdf_features = load_labeled_data(filter_in)
    model_configuration = ModelConfiguration()
    trainer = Trainer(pdf_features, model_configuration)
    trainer.train(TRAINED_MODEL_PATH)


if __name__ == "__main__":
    train()

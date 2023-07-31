from pathlib import Path

from ModelConfiguration import ModelConfiguration
from Trainer import Trainer
from config import TRAINED_MODEL_PATH
from load_labeled_data import load_labeled_data


def train(filter_in: str = None):
    Path(TRAINED_MODEL_PATH).parent.mkdir(exist_ok=True)
    pdf_features = load_labeled_data(filter_in)
    model_configuration = ModelConfiguration()
    trainer = Trainer(pdf_features, model_configuration)
    trainer.train(TRAINED_MODEL_PATH)


if __name__ == "__main__":
    train()

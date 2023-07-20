from os.path import join
from pathlib import Path

from ModelConfiguration import ModelConfiguration
from Trainer import Trainer
from load_labeled_data import load_labeled_data


def train():
    model_path = join(Path(__file__).parent.parent, "model", "pdf_tokens_type.model")
    Path(model_path).parent.mkdir(exist_ok=True)
    pdf_features = load_labeled_data()
    model_configuration = ModelConfiguration()
    trainer = Trainer(pdf_features, model_configuration)
    trainer.train(model_path)


if __name__ == "__main__":
    train()

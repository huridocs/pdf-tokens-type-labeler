from pdf_token_type_labels.load_labeled_data import load_labeled_data
from pdf_tokens_type_trainer.ModelConfiguration import ModelConfiguration
from pdf_tokens_type_trainer.TokenTypeTrainer import TokenTypeTrainer
from pdf_tokens_type_trainer.config import TRAINED_MODEL_PATH, PDF_LABELED_DATA_ROOT_PATH


def train():
    model_configuration = ModelConfiguration()
    train_pdf_features = load_labeled_data(PDF_LABELED_DATA_ROOT_PATH)
    trainer = TokenTypeTrainer(train_pdf_features, model_configuration)
    labels = [token.token_type.get_index() for token in trainer.loop_tokens()]
    print("training")
    trainer.train(TRAINED_MODEL_PATH, labels)


if __name__ == "__main__":
    train()

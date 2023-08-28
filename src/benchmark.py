from os.path import join
from pathlib import Path
from time import time

from sklearn.metrics import f1_score, accuracy_score

from pdf_features.PdfFeatures import PdfFeatures
from pdf_token_type_labels.load_labeled_data import load_labeled_data
from pdf_tokens_type_trainer.ModelConfiguration import ModelConfiguration
from pdf_tokens_type_trainer.TokenTypeTrainer import TokenTypeTrainer
from pdf_tokens_type_trainer.config import PDF_LABELED_DATA_ROOT_PATH

BENCHMARK_MODEL = join(Path(__file__).parent.parent, "model", "benchmark.model")


def train_for_benchmark():
    Path(BENCHMARK_MODEL).parent.mkdir(exist_ok=True)
    train_pdf_features = load_labeled_data(pdf_labeled_data_project_path=PDF_LABELED_DATA_ROOT_PATH, filter_in="train")
    model_configuration = ModelConfiguration()
    trainer = TokenTypeTrainer(train_pdf_features, model_configuration)
    print("training")
    trainer.train(BENCHMARK_MODEL)


def predict_for_benchmark():
    test_pdf_features = load_labeled_data(pdf_labeled_data_project_path=PDF_LABELED_DATA_ROOT_PATH, filter_in="test")
    trainer = TokenTypeTrainer(test_pdf_features, ModelConfiguration())
    truths = [token.token_type.get_index() for token in trainer.loop_tokens()]

    print("predicting")
    trainer.predict(BENCHMARK_MODEL)
    predictions = [token.prediction for token in trainer.loop_tokens()]
    return truths, predictions


def benchmark():
    train_for_benchmark()
    truths, predictions = predict_for_benchmark()

    f1 = round(f1_score(truths, predictions, average="macro") * 100, 2)
    accuracy = round(accuracy_score(truths, predictions) * 100, 2)
    print(f"F1 score {f1}%")
    print(f"Accuracy score {accuracy}%")


if __name__ == "__main__":
    start = time()
    print("start")
    benchmark()
    print("finished in", time() - start, "seconds")

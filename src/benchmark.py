from os.path import join
from pathlib import Path

from sklearn.metrics import f1_score, accuracy_score

from ModelConfiguration import ModelConfiguration
from Trainer import Trainer
from load_labeled_data import load_labeled_data
from pdf_features.PdfFeatures import PdfFeatures

BENCHMARK_MODEL = join(Path(__file__).parent.parent, "model", "benchmark.model")


def train_for_benchmark():
    Path(BENCHMARK_MODEL).parent.mkdir(exist_ok=True)
    train_pdf_features = load_labeled_data(filter_in="train")
    model_configuration = ModelConfiguration()
    trainer = Trainer(train_pdf_features, model_configuration)
    print("training")
    trainer.train(BENCHMARK_MODEL)


def get_predictions_for_benchmark(test_pdf_features: list[PdfFeatures]):
    trainer = Trainer(test_pdf_features, ModelConfiguration())
    print("predicting")
    return trainer.predict(BENCHMARK_MODEL)


def loop_tokens(test_pdf_features: list[PdfFeatures]):
    for pdf_features in test_pdf_features:
        for page, token in pdf_features.loop_tokens():
            yield token


def benchmark():
    train_for_benchmark()
    test_pdf_features = load_labeled_data(filter_in="test")
    predictions = [token.token_type.get_number() for token in get_predictions_for_benchmark(test_pdf_features)]
    truths = [token.token_type.get_number() for token in loop_tokens(test_pdf_features)]
    f1 = round(f1_score(truths, predictions, average="macro") * 100, 2)
    accuracy = round(accuracy_score(truths, predictions) * 100, 2)
    print(f"F1 score {f1 }%")
    print(f"Accuracy score {accuracy}%")


if __name__ == "__main__":
    benchmark()

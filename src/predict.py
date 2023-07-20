import typer

from ModelConfiguration import ModelConfiguration
from Trainer import Trainer

from pdf_features.PdfFeatures import PdfFeatures


def predict(pdf_path: str, model_path: str = None):
    pdf_features = PdfFeatures.from_pdf_path(pdf_path)
    trainer = Trainer([pdf_features], ModelConfiguration())
    results = trainer.predict(model_path)
    print([result.as_dict() for result in results])


if __name__ == "__main__":
    typer.run(predict)

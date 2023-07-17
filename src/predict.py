import typer

from ModelConfiguration import ModelConfiguration
from Trainer import Trainer
from download_models import pdf_tag_type_model_path

from pdf_features.PdfFeatures import PdfFeatures


def predict(pdf_path: str, model_path: str = pdf_tag_type_model_path):
    pdf_features = PdfFeatures.from_pdf(pdf_path)
    trainer = Trainer([pdf_features], ModelConfiguration())
    result = trainer.predict(model_path)
    print(result)


if __name__ == "__main__":
    typer.run(predict)

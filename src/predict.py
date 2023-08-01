import typer

from pdf_features.PdfFeatures import PdfFeatures
from pdf_tokens_type_trainer.ModelConfiguration import ModelConfiguration
from pdf_tokens_type_trainer.TokenTypeTrainer import TokenTypeTrainer


def predict(pdf_path: str, model_path: str = None):
    pdf_features = PdfFeatures.from_pdf_path(pdf_path)
    trainer = TokenTypeTrainer([pdf_features], ModelConfiguration())
    results = trainer.predict(model_path)
    print([result.to_dict() for result in results])


if __name__ == "__main__":
    typer.run(predict)

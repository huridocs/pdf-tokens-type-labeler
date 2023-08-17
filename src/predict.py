import typer

from pdf_features.PdfFeatures import PdfFeatures
from pdf_features.PdfSegment import PdfSegment
from pdf_token_type_labels.TokenType import TokenType
from pdf_tokens_type_trainer.ModelConfiguration import ModelConfiguration
from pdf_tokens_type_trainer.TokenTypeTrainer import TokenTypeTrainer


def predict(pdf_path: str, model_path: str = None):
    pdf_features = PdfFeatures.from_pdf_path(pdf_path)
    trainer = TokenTypeTrainer([pdf_features], ModelConfiguration())
    trainer.predict(model_path)

    predictions: list[PdfSegment] = list()

    for token in trainer.loop_tokens():
        token_type = TokenType.from_index(token.prediction)
        predictions.append(PdfSegment.from_pdf_token(token, token_type))

    print([prediction.to_dict() for prediction in predictions])


if __name__ == "__main__":
    typer.run(predict)

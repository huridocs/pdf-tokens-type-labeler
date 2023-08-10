from os.path import join, exists
from unittest import TestCase

from pdf_features.PdfFeatures import PdfFeatures
from pdf_token_type_labels.TokenType import TokenType
from pdf_tokens_type_trainer.TokenTypeTrainer import TokenTypeTrainer
from pdf_tokens_type_trainer.config import PDF_TOKENS_TYPE_ROOT_PATH


class TestTrainer(TestCase):
    def test_train_blank_pdf(self):
        pdf_features = PdfFeatures.from_pdf_path(join(PDF_TOKENS_TYPE_ROOT_PATH, "src", "test", "blank.pdf"))
        model_path = join(PDF_TOKENS_TYPE_ROOT_PATH, "model", "blank.model")
        trainer = TokenTypeTrainer([pdf_features])
        trainer.train(model_path)
        self.assertFalse(exists(model_path))

    def test_predict_blank_pdf(self):
        pdf_features = PdfFeatures.from_pdf_path(join(PDF_TOKENS_TYPE_ROOT_PATH, "src", "test", "blank.pdf"))
        trainer = TokenTypeTrainer([pdf_features])
        self.assertEqual([], trainer.predict())

    def test_predict(self):
        pdf_features = PdfFeatures.from_pdf_path(join(PDF_TOKENS_TYPE_ROOT_PATH, "src", "test", "test.pdf"))
        trainer = TokenTypeTrainer([pdf_features])
        types = trainer.predict()
        self.assertEqual(TokenType.TITLE, types[0].token_type)
        self.assertEqual("Document Big Centered Title", types[0].text_content)
        self.assertEqual(TokenType.TEXT, types[1].token_type)
        self.assertEqual(TokenType.TITLE, types[10].token_type)
        self.assertEqual("List Title", types[10].text_content)

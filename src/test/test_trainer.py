import shutil
from os.path import join, exists
from unittest import TestCase

from ModelConfiguration import ModelConfiguration
from TokenType import TokenType
from Trainer import Trainer
from config import ROOT_PATH
from pdf_features.PdfFeatures import PdfFeatures


class TestTrainer(TestCase):
    def test_train_blank_pdf(self):
        pdf_features = PdfFeatures.from_pdf_path(join(ROOT_PATH, "src", "test", "blank.pdf"))
        model_path = join(ROOT_PATH, "model", "blank.model")
        trainer = Trainer([pdf_features], ModelConfiguration())
        trainer.train(model_path)
        self.assertFalse(exists(model_path))

    def test_predict_blank_pdf(self):
        pdf_features = PdfFeatures.from_pdf_path(join(ROOT_PATH, "src", "test", "blank.pdf"))
        trainer = Trainer([pdf_features], ModelConfiguration())
        self.assertEqual([], trainer.predict())

    def test_train(self):
        labeled_data_path = join(ROOT_PATH, "labeled_data", "one_column_train")
        pdf_features_1 = PdfFeatures.from_poppler_etree(join(labeled_data_path, "cejil_staging1.xml"))
        pdf_features_2 = PdfFeatures.from_poppler_etree(join(labeled_data_path, "cejil_staging2.xml"))
        trainer = Trainer([pdf_features_1, pdf_features_2], ModelConfiguration())
        model_path = join(ROOT_PATH, "model", "test.model")
        shutil.rmtree(model_path, ignore_errors=True)
        trainer.train(model_path)
        self.assertTrue(exists(model_path))

    def test_predict(self):
        pdf_features = PdfFeatures.from_pdf_path(join(ROOT_PATH, "src", "test", "test.pdf"))
        trainer = Trainer([pdf_features], ModelConfiguration())
        types = trainer.predict()
        self.assertEqual("Document Big Centered Title", types[0].text_content)
        self.assertEqual(TokenType.TITLE, TokenType.from_text(types[0].token_type))
        self.assertEqual(TokenType.TEXT, TokenType.from_text(types[1].token_type))
        self.assertEqual(TokenType.TITLE, TokenType.from_text(types[10].token_type))
        self.assertEqual("List Title", types[10].text_content)

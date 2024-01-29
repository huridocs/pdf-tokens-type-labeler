from os.path import join
from pathlib import Path
from unittest import TestCase
from pdf_features.PdfFeatures import PdfFeatures


class TestPdfFeatures(TestCase):
    def test_blank_xml(self):
        pdf_features_empty = PdfFeatures.from_poppler_etree_content("", "")
        pdf_features_empty_list = PdfFeatures.from_poppler_etree_content("", "[]")
        self.assertNotEquals(pdf_features_empty, None)
        self.assertNotEquals(pdf_features_empty_list, None)

    def test_ocr_pdf(self):
        current_directory = Path(__file__).parent.resolve()
        pdf_features = PdfFeatures.from_pdf_path(join(current_directory, "ocr_pdf.pdf"))
        self.assertGreater(len(pdf_features.pages[0].tokens), 0)

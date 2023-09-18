from unittest import TestCase

from pdf_features.PdfFeatures import PdfFeatures


class TestPdfFeatures(TestCase):
    def test_blank_xml(self):
        pdf_features_empty = PdfFeatures.from_poppler_etree_content("", "")
        pdf_features_empty_list = PdfFeatures.from_poppler_etree_content("", "[]")
        self.assertNotEquals(pdf_features_empty, None)
        self.assertNotEquals(pdf_features_empty_list, None)
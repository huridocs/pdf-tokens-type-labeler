import json
import os
import subprocess
import tempfile
from os.path import join, exists
from pathlib import Path

from lxml import etree
from lxml.etree import ElementBase

from pdf_features.PdfFont import PdfFont
from pdf_features.PdfPage import PdfPage
from pdf_tokens_type_trainer.config import LABELED_DATA_PATH, XML_NAME, LABELS_FILE_NAME, LABELED_XML_PATH
from pdf_token_type_labels.TokenTypeLabels import TokenTypeLabels


class PdfFeatures:
    def __init__(
        self,
        pages: list[PdfPage],
        fonts: list[PdfFont],
        file_name="",
        file_type: str = "",
    ):
        self.pages = pages
        self.fonts = fonts
        self.file_name = file_name
        self.file_type = file_type

    def loop_tokens(self):
        for page, token in [(page, token) for page in self.pages for token in page.tokens]:
            yield page, token

    def set_token_types(self, token_type_labels: TokenTypeLabels):
        for page, token in self.loop_tokens():
            token.token_type = token_type_labels.get_token_type(token.page_number, token.bounding_box)

    @staticmethod
    def from_poppler_etree(file_path):
        file: str = open(file_path).read()
        file_bytes: bytes = file.encode("utf-8")
        root: ElementBase = etree.fromstring(file_bytes)

        fonts: list[PdfFont] = [PdfFont.from_poppler_etree(style_tag) for style_tag in root.findall(".//fontspec")]
        fonts_by_font_id: dict[str, PdfFont] = {font.font_id: font for font in fonts}
        tree_pages: list[ElementBase] = [tree_page for tree_page in root.findall(".//page")]
        pages: list[PdfPage] = [PdfPage.from_poppler_etree(tree_page, fonts_by_font_id) for tree_page in tree_pages]

        file_type: str = file_path.split("/")[-2]
        file_name: str = file_path.split("/")[-1]

        return PdfFeatures(pages, fonts, file_name, file_type)

    @staticmethod
    def from_pdf_path(pdf_path, xml_path: str = None):
        remove_xml = False if xml_path else True
        xml_path = xml_path if xml_path else join(tempfile.gettempdir(), "pdf_etree.xml")

        subprocess.run(["pdftohtml", "-i", "-xml", "-zoom", "1.0", pdf_path, xml_path])

        pdf_features = PdfFeatures.from_poppler_etree(xml_path)

        if remove_xml and exists(xml_path):
            os.remove(xml_path)

        return pdf_features

    @staticmethod
    def from_labeled_data(dataset: str, pdf_name: str):
        label_path = join(LABELED_DATA_PATH, dataset, pdf_name, LABELS_FILE_NAME)
        xml_path = join(LABELED_XML_PATH, pdf_name, XML_NAME)

        pdf_features = PdfFeatures.from_poppler_etree(xml_path)

        labels_text = Path(label_path).read_text()
        labels_dict = json.loads(labels_text)
        token_type_labels = TokenTypeLabels(**labels_dict)
        pdf_features.set_token_types(token_type_labels)

        return pdf_features

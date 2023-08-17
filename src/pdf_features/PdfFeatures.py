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
from pdf_token_type_labels.TokenTypeLabel import TokenTypeLabel
from pdf_tokens_type_trainer.config import (
    XML_NAME,
    LABELS_FILE_NAME,
)
from pdf_token_type_labels.TokenTypeLabels import TokenTypeLabels
from pdf_tokens_type_trainer.get_paths import (
    get_xml_path,
    get_token_type_labeled_data_path,
    get_paragraph_extraction_labeled_data_path,
)


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
        for page in self.pages:
            for token in page.tokens:
                yield page, token

    def set_token_types(self, token_type_labels: TokenTypeLabels):
        if not token_type_labels.pages:
            return

        for page, token in self.loop_tokens():
            token.token_type = token_type_labels.get_token_type(token.page_number, token.bounding_box)

    def set_paragraphs(self, paragraphs_extractions_labels: TokenTypeLabels):
        if not paragraphs_extractions_labels.pages:
            return

        labels_per_page = self.get_labels_per_page(paragraphs_extractions_labels)
        unassigned_token_index = 1000000
        for page, token in self.loop_tokens():
            for index, label in enumerate(labels_per_page[page.page_number]):
                if token.inside_label(label):
                    token.segment_no = index + 1
                    break

            token.segment_no = token.segment_no if token.segment_no else unassigned_token_index
            unassigned_token_index += 1

    def get_labels_per_page(self, paragraphs_extractions_labels):
        page_numbers = [page.page_number for page in self.pages]
        labels_per_page: dict[int, list[TokenTypeLabel]] = {page_number: list() for page_number in page_numbers}
        for page_labels in paragraphs_extractions_labels.pages:
            if page_labels.number in page_numbers:
                labels_per_page[page_labels.number].extend(page_labels.labels)
        return labels_per_page

    @staticmethod
    def from_poppler_etree(file_path: str | Path):
        try:
            file_content: str = open(file_path).read()
        except FileNotFoundError:
            return None

        return PdfFeatures.from_poppler_etree_content(file_path, file_content)

    @staticmethod
    def from_poppler_etree_content(file_path: str | Path, file_content: str):
        file_bytes: bytes = file_content.encode("utf-8")

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
    def from_labeled_data(pdf_labeled_data_project_path: str, dataset: str, pdf_name: str):
        xml_path = join(get_xml_path(pdf_labeled_data_project_path), pdf_name, XML_NAME)
        pdf_features = PdfFeatures.from_poppler_etree(xml_path)

        token_type_labeled_project_path = get_token_type_labeled_data_path(pdf_labeled_data_project_path)
        token_type_labels_path = join(token_type_labeled_project_path, dataset, pdf_name, LABELS_FILE_NAME)
        token_type_labels = PdfFeatures.load_token_type_labels(token_type_labels_path)
        pdf_features.set_token_types(token_type_labels)

        paragraph_extraction_labeled_project_path = get_paragraph_extraction_labeled_data_path(pdf_labeled_data_project_path)
        paragraph_extraction_labels_path = join(
            paragraph_extraction_labeled_project_path, dataset, pdf_name, LABELS_FILE_NAME
        )
        paragraphs_extractions_labels = PdfFeatures.load_token_type_labels(paragraph_extraction_labels_path)
        pdf_features.set_paragraphs(paragraphs_extractions_labels)

        return pdf_features

    @staticmethod
    def load_token_type_labels(path: str) -> TokenTypeLabels:
        if not exists(path):
            print(f"No labeled data for {path}")
            return TokenTypeLabels(pages=[])

        labels_text = Path(path).read_text()
        labels_dict = json.loads(labels_text)
        return TokenTypeLabels(**labels_dict)

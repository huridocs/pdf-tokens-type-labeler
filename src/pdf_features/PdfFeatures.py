import os
import subprocess
import tempfile
from os.path import join

from lxml.etree import ElementBase

from pdf_features.PdfFont import PdfFont
from pdf_features.PdfPage import PdfPage
from pdf_features.PdfTag import PdfTag

from lxml import etree


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

    def get_tags(self) -> list[PdfTag]:
        tags: list[PdfTag] = list()
        for page in self.pages:
            for tag in page.tags:
                tags.append(tag)

        return tags

    @staticmethod
    def from_pdf(pdf_path):
        xml_path = join(tempfile.gettempdir(), "pdf_etree.xml")
        subprocess.run(["pdftohtml", "-i", "-xml", "-zoom", "1.0", pdf_path, xml_path])
        pdf_features = PdfFeatures.from_poppler_etree(xml_path)
        os.remove(xml_path)
        return pdf_features

from lxml.etree import ElementBase

from pdf_features.PdfFont import PdfFont
from pdf_features.PdfToken import PdfToken


class PdfPage:
    def __init__(self, page_number: int, page_width: int, page_height: int, tokens: list[PdfToken]):
        self.page_number = page_number
        self.page_width = page_width
        self.page_height = page_height
        self.tokens = tokens

    @staticmethod
    def from_poppler_etree(xml_page: ElementBase, fonts_by_font_id: dict[str, PdfFont]):
        page_number = int(xml_page.attrib["number"])
        tokens = [
            PdfToken.from_poppler_etree(page_number, xml_tag, fonts_by_font_id[xml_tag.attrib["font"]])
            for xml_tag in xml_page.findall(".//text")
        ]
        tokens = [token for token in tokens if token.strip()]
        width = int(xml_page.attrib["width"])
        height = int(xml_page.attrib["height"])
        return PdfPage(page_number, width, height, tokens)

from typing import Self

from lxml.etree import ElementBase

from pdf_features.PdfFont import PdfFont
from pdf_features.Rectangle import Rectangle
from pdf_token_type_labels.TokenType import TokenType
from pdf_token_type_labels.TokenTypeLabel import TokenTypeLabel


class PdfToken:
    def __init__(
        self,
        page_number,
        tag_id: str,
        content: str,
        pdf_font: PdfFont,
        reading_order_no: int,
        segment_no: int,
        bounding_box: Rectangle,
        token_type: TokenType,
    ):
        self.page_number = int(page_number)
        self.id: str = tag_id
        self.content: str = content
        self.font: PdfFont = pdf_font
        self.reading_order_no: int = reading_order_no
        self.segment_no: int = segment_no
        self.bounding_box: Rectangle = bounding_box
        self.token_type: TokenType = token_type
        self.right_of_token_on_the_left = 0
        self.left_of_token_on_the_right = 0
        self.prediction = 0

    def same_line(self, tag: Self):
        if self.bounding_box.bottom < tag.bounding_box.top:
            return False

        if tag.bounding_box.bottom < self.bounding_box.top:
            return False

        return True

    @staticmethod
    def from_poppler_etree(page_number: int, xml_tag: ElementBase, pdf_font: PdfFont):
        if "id" in xml_tag.attrib:
            tag_id = xml_tag.attrib["id"]
        else:
            tag_id = "tag"

        content = "".join(xml_tag.itertext()).strip()
        reading_order_no = int(xml_tag.attrib["reading_order_no"]) if "reading_order_no" in xml_tag.attrib else -1
        segment_no = int(xml_tag.attrib["segment_no"]) if "segment_no" in xml_tag.attrib else -1
        bounding_box = Rectangle.from_poppler_tag_etree(xml_tag)
        token_type = TokenType.TEXT

        return PdfToken(page_number, tag_id, content, pdf_font, reading_order_no, segment_no, bounding_box, token_type)

    def inside_label(self, label: TokenTypeLabel):
        label_bounding_box = Rectangle.from_width_height(
            left=label.left, top=label.top, width=label.width, height=label.height
        )

        return self.bounding_box.get_intersection_percentage(label_bounding_box) > 50

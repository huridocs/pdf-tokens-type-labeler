from typing import Union

from lxml.etree import ElementBase
from pydantic import BaseModel

from pdf_features.Rectangle import Rectangle
from pdf_token_type_labels.ParagraphType import ParagraphType
from pdf_token_type_labels.TableOfContentType import TableOfContentType
from pdf_token_type_labels.TokenType import TokenType


class TokenTypeLabel(BaseModel):
    top: int
    left: int
    width: int
    height: int
    token_type: Union[TokenType, ParagraphType, TableOfContentType, int]

    def intersection_percentage(self, token_bounding_box: Rectangle):
        label_bounding_box = Rectangle(
            left=self.left, top=self.top, right=self.left + self.width, bottom=self.top + self.height
        )
        return label_bounding_box.get_intersection_percentage(token_bounding_box)

    def get_location_discrepancy(self, token_bounding_box: Rectangle):
        coordinates_discrepancy: int = abs(self.left - token_bounding_box.left) + abs(self.top - token_bounding_box.top)
        size_discrepancy: int = abs(self.height - token_bounding_box.height) + abs(self.width - token_bounding_box.width)
        return coordinates_discrepancy + size_discrepancy

    def area(self):
        return self.width * self.height

    @staticmethod
    def from_text_element(text_element: ElementBase):
        return TokenTypeLabel(
            top=text_element.attrib["top"],
            left=text_element.attrib["left"],
            width=text_element.attrib["width"],
            height=text_element.attrib["height"],
            token_type=TokenType.from_text(text_element.attrib["tag_type"]),
        )

    @staticmethod
    def from_text_elements(text_elements: list[ElementBase]):
        top = min([int(x.attrib["top"]) for x in text_elements])
        left = min([int(x.attrib["left"]) for x in text_elements])
        bottom = max([int(x.attrib["top"]) + int(x.attrib["height"]) for x in text_elements])
        right = max([int(x.attrib["left"]) + int(x.attrib["width"]) for x in text_elements])

        return TokenTypeLabel(
            top=top, left=left, width=int(right - left), height=int(bottom - top), token_type=ParagraphType.PARAGRAPH
        )

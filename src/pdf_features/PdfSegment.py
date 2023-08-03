from pdf_features.PdfToken import PdfToken
from pdf_features.Rectangle import Rectangle
from token_type_labels.TokenType import TokenType


class PdfSegment:
    def __init__(self, page_number: int, bounding_box: Rectangle, text_content: str, token_type: TokenType):
        self.page_number = page_number
        self.bounding_box = bounding_box
        self.text_content = text_content
        self.token_type = token_type

    @staticmethod
    def from_pdf_token(pdf_token: PdfToken, token_type: TokenType):
        return PdfSegment(pdf_token.page_number, pdf_token.bounding_box, pdf_token.content, token_type)

    def to_dict(self):
        return {
            "page_number": self.page_number,
            "bounding_box": self.bounding_box.to_dict(),
            "text_content": self.text_content,
            "token_type": self.token_type.value,
        }

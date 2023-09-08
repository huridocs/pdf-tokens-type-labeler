from pdf_features.PdfToken import PdfToken
from pdf_features.Rectangle import Rectangle
from pdf_token_type_labels.TokenType import TokenType


class Token:
    def __init__(self, page_number: int, bounding_box: Rectangle, text_content: str, token_type: TokenType):
        self.page_number = page_number
        self.bounding_box = bounding_box
        self.text_content = text_content
        self.token_type = token_type

    @staticmethod
    def from_pdf_token(pdf_token: PdfToken, token_type: TokenType):
        return Token(pdf_token.page_number, pdf_token.bounding_box, pdf_token.content, token_type)

    @staticmethod
    def from_pdf_tokens(pdf_tokens: list[PdfToken]):
        text: str = " ".join([pdf_token.content for pdf_token in pdf_tokens])
        bounding_boxes = [pdf_token.bounding_box for pdf_token in pdf_tokens]
        return Token(
            pdf_tokens[0].page_number, Rectangle.merge_rectangles(bounding_boxes), text, pdf_tokens[0].token_type
        )

    def to_dict(self):
        return {
            "page_number": self.page_number,
            "bounding_box": self.bounding_box.to_dict(),
            "text_content": self.text_content,
            "token_type": self.token_type.value,
        }

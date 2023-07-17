from TokenType import TokenType
from pdf_features.PdfTag import PdfTag
from pdf_features.Rectangle import Rectangle


class PdfSegment:
    def __init__(
            self,
            page_number: int,
            bounding_box: Rectangle,
            text_content: str,
            token_type: TokenType
    ):
        self.page_number = page_number
        self.bounding_box = bounding_box
        self.text_content = text_content
        self.token_type = token_type

    @staticmethod
    def from_pdf_tag(pdf_tag: PdfTag):
        return PdfSegment(pdf_tag.page_number, pdf_tag.bounding_box, pdf_tag.content, pdf_tag.token_type)

    def dict(self):
        return {"page_number": self.page_number,
                "bounding_box": self.bounding_box,
                "text_content": self.text_content,
                "token_type": self.token_type}

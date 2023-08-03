from pydantic import BaseModel

from token_type_labels.Page import Page
from pdf_features.Rectangle import Rectangle
from token_type_labels.TokenType import TokenType


class TokenTypeLabels(BaseModel):
    pages: list[Page] = list()

    def get_token_type(self, page_number: int, token_bounding_box: Rectangle):
        for page in self.pages:
            if page.number != page_number:
                continue

            return page.get_token_type(token_bounding_box)

        return TokenType.TEXT

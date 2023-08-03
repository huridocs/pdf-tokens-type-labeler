from pydantic import BaseModel

from pdf_features.Rectangle import Rectangle
from pdf_token_type_labels.TokenType import TokenType
from pdf_token_type_labels.TokenTypeLabel import TokenTypeLabel


class Page(BaseModel):
    number: int
    labels: list[TokenTypeLabel]

    def get_token_type(self, token_bounding_box: Rectangle):
        intersection_percentage = 0
        token_type = TokenType.TEXT
        sorted_labels_by_area = sorted(self.labels, key=lambda x: x.area())
        for label in sorted_labels_by_area:
            if label.intersection_percentage(token_bounding_box) > intersection_percentage:
                intersection_percentage = label.intersection_percentage(token_bounding_box)
                token_type = label.token_type
            if intersection_percentage > 95:
                return token_type

        return token_type

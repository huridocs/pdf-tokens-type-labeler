from pydantic import BaseModel

from pdf_features.Rectangle import Rectangle
from token_type_labels.TokenType import TokenType


class TokenTypeLabel(BaseModel):
    top: int
    left: int
    width: int
    height: int
    token_type: TokenType

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

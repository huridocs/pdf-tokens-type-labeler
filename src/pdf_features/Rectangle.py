import math
from lxml.etree import ElementBase


class Rectangle:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.width = self.right - self.left
        self.height = self.bottom - self.top

    @staticmethod
    def from_segment_dict(paragraph: dict[str, any]) -> "Rectangle":
        return Rectangle(
            paragraph["left"],
            paragraph["top"],
            paragraph["left"] + paragraph["width"],
            paragraph["top"] + paragraph["height"],
        )

    @staticmethod
    def merge_rectangles(rectangles: list["Rectangle"]) -> "Rectangle":
        left = min([rectangle.left for rectangle in rectangles])
        top = min([rectangle.top for rectangle in rectangles])
        right = max([rectangle.right for rectangle in rectangles])
        bottom = max([rectangle.bottom for rectangle in rectangles])

        return Rectangle(left, top, right, bottom)

    @staticmethod
    def from_pdftags(tags) -> "Rectangle":
        return Rectangle.merge_rectangles(
            [
                Rectangle(
                    tag.bounding_box.left,
                    tag.bounding_box.top,
                    tag.bounding_box.right,
                    tag.bounding_box.bottom,
                )
                for tag in tags
            ]
        )

    @staticmethod
    def is_inside_tag(big_rectangle: "Rectangle", small_rectangle: "Rectangle") -> bool:
        if big_rectangle.left > small_rectangle.right:
            return False
        elif big_rectangle.right < small_rectangle.left:
            return False
        elif big_rectangle.bottom < small_rectangle.top:
            return False
        elif big_rectangle.top > small_rectangle.bottom:
            return False

        return True

    @staticmethod
    def from_poppler_tag_etree(tag: ElementBase) -> "Rectangle":
        x_min = int(tag.attrib["left"])
        y_min = int(tag.attrib["top"])
        x_max = x_min + int(tag.attrib["width"])
        y_max = y_min + int(tag.attrib["height"])

        return Rectangle(x_min, y_min, x_max, y_max)

import os
import sys

from lxml.etree import ElementBase

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class Rectangle:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.fix_wrong_areas()
        self.width = self.right - self.left
        self.height = self.bottom - self.top

    @staticmethod
    def from_poppler_tag_etree(tag: ElementBase) -> "Rectangle":
        x_min = int(tag.attrib["left"])
        y_min = int(tag.attrib["top"])
        x_max = x_min + int(tag.attrib["width"])
        y_max = y_min + int(tag.attrib["height"])

        return Rectangle(x_min, y_min, x_max, y_max)

    def fix_wrong_areas(self):
        if self.right == self.left:
            self.left -= 1
            self.right += 1

        if self.top == self.bottom:
            self.top -= 1
            self.bottom += 1

        if self.right < self.left:
            self.right, self.left = self.left, self.right

        if self.bottom < self.top:
            self.top, self.bottom = self.bottom, self.top

    def get_intersection_percentage(self, rectangle: "Rectangle"):
        x1 = max(self.left, rectangle.left)
        y1 = max(self.top, rectangle.top)
        x2 = min(self.right, rectangle.right)
        y2 = min(self.bottom, rectangle.bottom)

        if x2 <= x1 or y2 <= y1:
            return 0

        return 100 * (x2 - x1) * (y2 - y1) / self.area()

    def area(self):
        return self.width * self.height

    def to_dict(self):
        return {"top": self.top, "left": self.left, "right": self.right, "bottom": self.bottom}

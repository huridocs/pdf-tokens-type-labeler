from enum import Enum


class TagType(Enum):
    FORMULA = 0
    FOOTNOTE = 1
    LIST = 2
    TABLE = 3
    FIGURE = 4
    TITLE = 5
    TEXT = 6

    @staticmethod
    def from_text(text: str):
        try:
            return TagType[text.upper()]
        except KeyError:
            return TagType.TEXT

    @staticmethod
    def from_value(value: int):
        try:
            return TagType(value).name.lower()
        except ValueError:
            return TagType.TEXT.name.lower()

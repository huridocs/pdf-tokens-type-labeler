from enum import Enum


class TokenType(Enum):
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
            return TokenType[text.upper()]
        except KeyError:
            return TokenType.TEXT

    @staticmethod
    def from_value(value: int):
        try:
            return TokenType(value).name.lower()
        except ValueError:
            return TokenType.TEXT.name.lower()

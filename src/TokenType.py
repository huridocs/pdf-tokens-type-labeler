from enum import Enum


class TokenType(Enum):
    FORMULA = 0
    FOOTNOTE = 1
    LIST = 2
    TABLE = 3
    CODE = 4
    FIGURE = 5
    TITLE = 6
    TEXT = 7

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

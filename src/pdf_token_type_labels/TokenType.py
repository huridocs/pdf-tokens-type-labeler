from enum import Enum


class TokenType(Enum):
    FORMULA = "FORMULA"
    FOOTNOTE = "FOOTNOTE"
    LIST = "LIST"
    TABLE = "TABLE"
    FIGURE = "FIGURE"
    TITLE = "TITLE"
    TEXT = "TEXT"
    HEADER = "HEADER"
    PAGE_NUMBER = "PAGE_NUMBER"
    IMAGE_CAPTION = "IMAGE_CAPTION"
    FOOTER = "FOOTER"
    TABLE_OF_CONTENT = "TABLE_OF_CONTENT"
    MARK = "MARK"

    @staticmethod
    def from_text(text: str):
        try:
            return TokenType[text.upper()]
        except KeyError:
            return TokenType.TEXT

    @staticmethod
    def from_index(index: int):
        try:
            return list(TokenType)[index]
        except IndexError:
            return TokenType.TEXT.name.lower()

    def get_index(self) -> int:
        return list(TokenType).index(self)

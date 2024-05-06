from enum import Enum


class TokenType(Enum):
    FORMULA = "Formula"
    FOOTNOTE = "Footnote"
    LIST_ITEM = "ListItem"
    TABLE = "Table"
    PICTURE = "Picture"
    TITLE = "Title"
    TEXT = "Text"
    PAGE_HEADER = "PageHeader"
    SECTION_HEADER = "SectionHeader"
    CAPTION = "Caption"
    PAGE_FOOTER = "PageFooter"

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

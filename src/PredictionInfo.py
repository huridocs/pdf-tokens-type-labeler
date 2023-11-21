from pdf_features.PdfFeatures import PdfFeatures
from pdf_features.PdfToken import PdfToken
from pdf_token_type_labels.TokenType import TokenType


class PredictionInfo:
    def __init__(self, pdf_features: PdfFeatures, token: PdfToken):
        self.file_type: str = pdf_features.file_type
        self.file_name: str = pdf_features.file_name
        self.page_number: int = token.page_number
        self.actual_label: str = token.token_type.value
        self.prediction: str = TokenType.from_index(token.prediction).value

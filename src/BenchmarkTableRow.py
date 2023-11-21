from PredictionInfo import PredictionInfo
from pdf_token_type_labels.TokenType import TokenType


class BenchmarkTableRow:
    def __init__(self, predictions_for_file_type: list[PredictionInfo], mistakes_for_file_type: list[PredictionInfo]):
        self.file_type: str = predictions_for_file_type[0].file_type
        self.label_counts: dict[str, int] = {token_type.value: 0 for token_type in TokenType}
        self.mistake_counts: dict[str, int] = {token_type.value: 0 for token_type in TokenType}
        self.find_label_counts(predictions_for_file_type)
        self.find_mistake_counts(mistakes_for_file_type)

    def find_label_counts(self, predictions_for_file_type: list[PredictionInfo]):
        for prediction in predictions_for_file_type:
            self.label_counts[prediction.actual_label] += 1

    def find_mistake_counts(self, mistakes_for_file_type: list[PredictionInfo]):
        for mistake in mistakes_for_file_type:
            self.mistake_counts[mistake.actual_label] += 1

    def get_row_values(self):
        row_values = [self.file_type]
        for token_type in TokenType:
            mistake_count: int = self.mistake_counts[token_type.value]
            label_count: int = self.label_counts[token_type.value]
            success_percentage: float = 100.0 if label_count == 0 else 100 - (100 * mistake_count / label_count)
            row_values.append(f"{mistake_count}/{label_count} ({round(success_percentage, 2)}%)")
        return row_values

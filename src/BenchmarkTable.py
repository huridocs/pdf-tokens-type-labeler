from tabulate import tabulate
from BenchmarkTableRow import BenchmarkTableRow
from PredictionInfo import PredictionInfo
from pdf_features.PdfFeatures import PdfFeatures
from pdf_token_type_labels.TokenType import TokenType


class BenchmarkTable:
    def __init__(self, pdfs_features: list[PdfFeatures], total_time: float):
        self.pdfs_features: list[PdfFeatures] = pdfs_features
        self.total_time = total_time
        self.prediction_info_list: list[PredictionInfo] = []
        self.mistakes: list[PredictionInfo] = []
        self.get_prediction_info_list()
        self.get_mistakes()

    def get_prediction_info_list(self):
        for pdf_features in self.pdfs_features:
            for page, token in pdf_features.loop_tokens():
                self.prediction_info_list.append(PredictionInfo(pdf_features, token))

    def get_mistakes(self):
        for prediction_info in self.prediction_info_list:
            if prediction_info.prediction != prediction_info.actual_label:
                self.mistakes.append(prediction_info)

    def get_benchmark_table_rows(self):
        benchmark_table_rows: list[BenchmarkTableRow] = []
        file_types = set(prediction.file_type for prediction in self.prediction_info_list)
        for file_type in file_types:
            predictions_for_file_type = [info for info in self.prediction_info_list if info.file_type == file_type]
            mistakes_for_file_type = [mistake for mistake in self.mistakes if mistake.file_type == file_type]
            benchmark_table_rows.append(BenchmarkTableRow(predictions_for_file_type, mistakes_for_file_type))
        return benchmark_table_rows

    def prepare_benchmark_table(self):
        table_headers = ["File Type"]
        table_headers += [token_type.value for token_type in TokenType]
        benchmark_table_rows = self.get_benchmark_table_rows()
        mistake_count, label_count = len(self.mistakes), len(self.prediction_info_list)
        average_accuracy = 100 - (100 * mistake_count / len(self.prediction_info_list))
        with open("../results/benchmark_table.txt", "w") as benchmark_file:
            table_rows = [table_row.get_row_values() for table_row in benchmark_table_rows]
            benchmark_table = (
                tabulate(tabular_data=table_rows, headers=table_headers)
                + "\n\n"
                + f"Average Accuracy: {mistake_count}/{label_count} ({round(average_accuracy, 2)}%)"
                + "\n"
                + f"Total Time: {round(self.total_time, 2)}"
            )
            benchmark_file.write(benchmark_table)

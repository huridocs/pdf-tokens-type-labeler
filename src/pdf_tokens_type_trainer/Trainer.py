import lightgbm as lgb
import numpy as np
from tqdm import tqdm

from pdf_features.PdfFeatures import PdfFeatures
from pdf_features.PdfFont import PdfFont
from pdf_features.PdfSegment import PdfSegment
from pdf_features.PdfToken import PdfToken
from pdf_features.Rectangle import Rectangle
from pdf_features.token_type.TokenType import TokenType
from pdf_tokens_type_trainer.ModelConfiguration import ModelConfiguration
from pdf_tokens_type_trainer.TokenFeatures import TokenFeatures
from pdf_tokens_type_trainer.download_models import pdf_tokens_type_model


class Trainer:
    def __init__(self, pdf_features: list[PdfFeatures], model_configuration: ModelConfiguration):
        self.model_configuration = model_configuration
        self.pdf_features = pdf_features

    def get_model_input(self):
        features_rows = []
        y = np.array([])

        contex_size = self.model_configuration.context_size
        for token_features, page in self.loop_pages():
            page_tokens = [
                self.get_padding_token(segment_number=i - 999999, page_number=page.page_number) for i in range(contex_size)
            ]
            page_tokens += page.tokens
            page_tokens += [
                self.get_padding_token(segment_number=999999 + i, page_number=page.page_number) for i in range(contex_size)
            ]

            tokens_indexes = range(contex_size, len(page_tokens) - contex_size)
            page_features = [self.get_context_features(token_features, page_tokens, i) for i in tokens_indexes]
            features_rows.extend(page_features)

            y = np.append(y, [page_tokens[i].token_type.get_index() for i in tokens_indexes])

        return self.features_rows_to_x(features_rows), y

    @staticmethod
    def features_rows_to_x(features_rows):
        if not features_rows:
            return np.zeros((0, 0))

        x = np.zeros(((len(features_rows)), len(features_rows[0])))
        for i, v in enumerate(features_rows):
            x[i] = v
        return x

    def train(self, model_path: str):
        print(f"Getting model input")
        x_train, y_train = self.get_model_input()

        if not x_train.any():
            print("No data for training")
            return

        lgb_train = lgb.Dataset(x_train, y_train)
        print(f"Training")

        gbm = lgb.train(self.model_configuration.dict(), lgb_train)
        print(f"Saving")
        gbm.save_model(model_path, num_iteration=gbm.best_iteration)

    def loop_pages(self):
        for pdf_features in tqdm(self.pdf_features):
            token_features = TokenFeatures(pdf_features)

            for page in pdf_features.pages:
                if not page.tokens:
                    continue

                yield token_features, page

    @staticmethod
    def get_padding_token(segment_number: int, page_number: int):
        return PdfToken(
            page_number,
            "pad_token",
            "",
            PdfFont("pad_font_id", False, False, 0.0),
            segment_number,
            segment_number,
            Rectangle(0, 0, 0, 0),
            TokenType.TEXT,
        )

    def get_context_features(self, token_features: TokenFeatures, page_tokens: list[PdfToken], token_index: int):
        token_row_features = []
        first_token_from_context = token_index - self.model_configuration.context_size
        for i in range(self.model_configuration.context_size * 2):
            first_token = page_tokens[first_token_from_context + i]
            second_token = page_tokens[first_token_from_context + i + 1]
            token_row_features.extend(token_features.get_features(first_token, second_token, page_tokens))

        return token_row_features

    def predict(self, model_path: str = None) -> list[PdfSegment]:
        model_path = model_path if model_path else pdf_tokens_type_model
        x, _ = self.get_model_input()
        results: list[PdfSegment] = list()

        if not x.any():
            return results

        lightgbm_model = lgb.Booster(model_file=model_path)
        predictions = lightgbm_model.predict(x)
        predictions_assigned = 0
        for token_features, page in self.loop_pages():
            for token, prediction in zip(
                page.tokens, predictions[predictions_assigned : predictions_assigned + len(page.tokens)]
            ):
                results.append(PdfSegment.from_pdf_token(token, TokenType.from_index(int(np.argmax(prediction)))))

            predictions_assigned += len(page.tokens)

        return results
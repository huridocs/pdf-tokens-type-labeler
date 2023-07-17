import numpy as np
import lightgbm as lgb
from tqdm import tqdm

from ModelConfiguration import ModelConfiguration
from TokenType import TokenType
from TokenFeatures import TokenFeatures
from pdf_features.PdfFeatures import PdfFeatures
from pdf_features.PdfFont import PdfFont
from pdf_features.PdfSegment import PdfSegment
from pdf_features.PdfTag import PdfTag
from pdf_features.Rectangle import Rectangle


class Trainer:
    def __init__(self, pdf_features: list[PdfFeatures], model_configuration: ModelConfiguration):
        self.model_configuration = model_configuration
        self.pdf_features = pdf_features
        self.tag_type_counts = {}
        self.wrong_prediction_counts = {}

    def get_model_input(self):
        features_rows = []
        y = np.array([])

        contex_size = self.model_configuration.context_size
        for token_features, page in self.loop_pages():
            page_tags = [
                self.get_pad_tag(segment_number=i - 999999, page_number=page.page_number) for i in range(contex_size)
            ]
            page_tags += page.tags
            page_tags += [
                self.get_pad_tag(segment_number=999999 + i, page_number=page.page_number) for i in range(contex_size)
            ]

            tags_indexes = range(contex_size, len(page_tags) - contex_size)
            page_features = [self.get_context_features(token_features, page_tags, i) for i in tags_indexes]
            features_rows.extend(page_features)

            y = np.append(y, [page_tags[i].token_type.value for i in tags_indexes])

        return self.features_rows_to_x(features_rows), y

    @staticmethod
    def features_rows_to_x(features_rows):
        x = np.zeros(((len(features_rows)), len(features_rows[0])))
        for i, v in enumerate(features_rows):
            x[i] = v
        return x

    def train(self, model_path: str):
        print(f"Getting model input")
        x_train, y_train = self.get_model_input()

        lgb_train = lgb.Dataset(x_train, y_train)
        print(f"Training")

        gbm = lgb.train(self.model_configuration.dict(), lgb_train)
        print(f"Saving")
        gbm.save_model(model_path, num_iteration=gbm.best_iteration)

    def loop_pages(self):
        for pdf_features in tqdm(self.pdf_features):
            token_features = TokenFeatures(pdf_features)

            for page in pdf_features.pages:
                if not page.tags:
                    continue

                yield token_features, page

    @staticmethod
    def get_pad_tag(segment_number: int, page_number: int):
        return PdfTag(
            page_number,
            "pad_tag",
            "",
            PdfFont("pad_font_id", False, False, 0.0),
            segment_number,
            segment_number,
            Rectangle(0, 0, 0, 0),
            TokenType.TEXT,
        )

    def get_context_features(self, token_features: TokenFeatures, page_tags: list[PdfTag], tag_index: int):
        tag_features = []
        first_tag_from_context = tag_index - self.model_configuration.context_size
        for i in range(self.model_configuration.context_size * 2):
            first_tag = page_tags[first_tag_from_context + i]
            second_tag = page_tags[first_tag_from_context + i + 1]
            tag_features.extend(token_features.get_features(first_tag, second_tag, page_tags))

        return tag_features

    def predict(self, model_path):
        x, _ = self.get_model_input()
        lightgbm_model = lgb.Booster(model_file=model_path)
        predictions = lightgbm_model.predict(x)
        results: list[PdfSegment] = list()
        predictions_assigned = 0
        for token_features, page in self.loop_pages():
            for tag, prediction in zip(page.tags, predictions[predictions_assigned:predictions_assigned + len(page.tags)]):
                tag.token_type = TokenType.from_value(prediction)
                results.append(PdfSegment.from_pdf_tag(tag))

            predictions_assigned += len(page.tags)

        return results

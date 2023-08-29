import ast
import string
from collections import Counter
from statistics import mode

from numpy import unique

from pdf_features.PdfFeatures import PdfFeatures
from pdf_features.PdfToken import PdfToken
from pdf_tokens_type_trainer.download_models import letter_corpus_path


class TokenFeatures:
    def __init__(self, pdfs_features: PdfFeatures):
        self.pdfs_features = pdfs_features
        self.tuples_to_check: list[tuple[PdfToken, PdfToken]] = list()

        self.letter_corpus: dict[str, int] = self.get_letter_corpus()
        self.len_letter_corpus = len(unique(list(self.letter_corpus.values())))

        self.lines_space_mode: float = 0
        self.right_space_mode: float = 0
        self.font_size_mode: float = 0

        self.get_modes()
        self.get_mode_font()
        self.get_left_right_block()

    @staticmethod
    def get_letter_corpus():
        with open(letter_corpus_path, "r") as corpus_file:
            corpus_contents = corpus_file.read()
            return ast.literal_eval(corpus_contents)

    def get_modes(self):
        line_spaces, right_spaces = [0], [0]

        for page, token in self.pdfs_features.loop_tokens():
            top, bottom = token.bounding_box.top, token.bounding_box.bottom
            left, right = token.bounding_box.left, token.bounding_box.right

            on_the_bottom = [page_token for page_token in page.tokens if page_token.bounding_box.bottom < top]

            on_the_right = [
                line_token
                for line_token in self.get_same_line_tokens(token, page.tokens)
                if right < line_token.bounding_box.left
            ]

            if len(on_the_bottom):
                line_spaces.append(min(map(lambda x: int(x.bounding_box.top - bottom), on_the_bottom)))

            if not on_the_right:
                right_spaces.append(int(right))

        self.lines_space_mode = mode(line_spaces)
        self.right_space_mode = int(self.pdfs_features.pages[0].page_width - mode(right_spaces))

    def get_mode_font(self):
        fonts_counter: Counter = Counter()
        for page, token in self.pdfs_features.loop_tokens():
            fonts_counter.update([token.font.font_id])

        if len(fonts_counter.most_common()) == 0:
            return

        font_mode_id = fonts_counter.most_common()[0][0]
        font_mode_token = list(filter(lambda x: x.font_id == font_mode_id, self.pdfs_features.fonts))
        if font_mode_token:
            self.font_size_mode: float = float(font_mode_token[0].font_size)

    def get_features(self, token_1: PdfToken, token_2: PdfToken, page_tokens: list[PdfToken]):
        same_font = True if token_1.font.font_id == token_2.font.font_id else False

        return (
            [
                same_font,
                self.font_size_mode / 100,
                len(token_1.content),
                len(token_2.content),
                token_1.content.count(" "),
                token_2.content.count(" "),
                sum(character in string.punctuation for character in token_1.content),
                sum(character in string.punctuation for character in token_2.content),
            ]
            + self.get_position_features(token_1, token_2, page_tokens)
            + self.get_first_letter_last_letter_one_hot_encoding(token_1)
            + self.get_first_letter_last_letter_one_hot_encoding(token_2)
        )

    def get_position_features(self, token_1: PdfToken, token_2: PdfToken, page_tokens):
        left_1 = token_1.bounding_box.left
        right_1 = token_1.bounding_box.right
        height_1 = token_1.bounding_box.height
        width_1 = token_1.bounding_box.width

        left_2 = token_2.bounding_box.left
        right_2 = token_2.bounding_box.right
        height_2 = token_2.bounding_box.height
        width_2 = token_2.bounding_box.width

        right_gap_1, left_gap_2 = token_1.left_of_token_on_the_right - right_1, left_2 - token_2.right_of_token_on_the_left

        absolute_right_1 = max(right_1, token_1.right_of_token_on_the_right)
        absolute_right_2 = max(right_2, token_2.right_of_token_on_the_right)

        absolute_left_1 = min(left_1, token_1.left_of_token_on_the_left)
        absolute_left_2 = min(left_2, token_2.left_of_token_on_the_left)

        right_distance, left_distance, height_difference = left_2 - left_1 - width_1, left_1 - left_2, height_1 - height_2

        top_distance = token_2.bounding_box.top - token_1.bounding_box.top - height_1
        top_distance_gaps = self.get_top_distance_gap(token_1, token_2, page_tokens)

        start_lines_differences = absolute_left_1 - absolute_left_2
        end_lines_difference = abs(absolute_right_1 - absolute_right_2)

        return [
            absolute_right_1,
            token_1.bounding_box.top,
            right_1,
            width_1,
            height_1,
            token_2.bounding_box.top,
            right_2,
            width_2,
            height_2,
            right_distance,
            left_distance,
            right_gap_1,
            left_gap_2,
            height_difference,
            top_distance,
            top_distance - self.lines_space_mode,
            top_distance_gaps,
            top_distance - height_1,
            end_lines_difference,
            start_lines_differences,
            self.lines_space_mode - top_distance_gaps,
            self.right_space_mode - absolute_right_1,
        ]

    @staticmethod
    def get_top_distance_gap(token_1: PdfToken, token_2: PdfToken, page_tokens):
        top_distance = token_2.bounding_box.top - token_1.bounding_box.top - token_1.bounding_box.height
        tokens_in_the_middle = [
            token
            for token in page_tokens
            if token_1.bounding_box.bottom <= token.bounding_box.top < token_2.bounding_box.top
        ]

        gap_middle_bottom = 0
        gap_middle_top = 0

        if tokens_in_the_middle:
            tokens_in_the_middle_top = min([token.bounding_box.top for token in tokens_in_the_middle])
            tokens_in_the_middle_bottom = max([token.bounding_box.bottom for token in tokens_in_the_middle])
            gap_middle_top = tokens_in_the_middle_top - token_1.bounding_box.top - token_1.bounding_box.height
            gap_middle_bottom = token_2.bounding_box.top - tokens_in_the_middle_bottom

        top_distance_gaps = top_distance - (gap_middle_bottom - gap_middle_top)
        return top_distance_gaps

    def get_left_right_block(self):
        for page, token in self.pdfs_features.loop_tokens():
            left, right = token.bounding_box.left, token.bounding_box.right

            token.left_of_tokens_on_the_left = left

            same_line_tokens = self.get_same_line_tokens(token, page.tokens)

            on_the_left = [each_token for each_token in same_line_tokens if each_token.bounding_box.right < right]
            on_the_right = [each_token for each_token in same_line_tokens if left < each_token.bounding_box.left]

            if on_the_left:
                token.right_of_tokens_on_the_left = max([x.bounding_box.right for x in on_the_left])
                token.left_of_tokens_on_the_left = min([x.bounding_box.left for x in on_the_left])

            if on_the_right:
                token.left_of_tokens_on_the_right = min([x.bounding_box.left for x in on_the_right])
                token.right_of_tokens_on_the_right = max([x.bounding_box.right for x in on_the_right])

    @staticmethod
    def get_same_line_tokens(token, tokens):
        top, height = token.bounding_box.top, token.bounding_box.height

        same_line_tokens = [
            each_token
            for each_token in tokens
            if top <= each_token.bounding_box.top < (top + height) or top < each_token.bounding_box.bottom <= (top + height)
        ]

        return same_line_tokens

    def get_first_letter_last_letter_one_hot_encoding(self, token: PdfToken):
        token_first_letter = [-1 if token.id == "pad_token" else 0] * self.len_letter_corpus
        token_last_letter = [-1 if token.id == "pad_token" else 0] * self.len_letter_corpus

        if token.content and token.content[0] in self.letter_corpus.keys():
            token_first_letter[self.letter_corpus[token.content[0]]] = 1

        if token.content and token.content[-1] in self.letter_corpus.keys():
            token_last_letter[self.letter_corpus[token.content[-1]]] = 1

        return token_first_letter + token_last_letter

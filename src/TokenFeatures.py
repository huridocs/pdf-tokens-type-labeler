import ast
import string
from collections import Counter
from statistics import mode

from numpy import unique

from pdf_features.PdfFeatures import PdfFeatures
from pdf_features.PdfTag import PdfTag
from download_models import letter_corpus_path


class TokenFeatures:
    def __init__(self, pdf_features: PdfFeatures):
        self.pdf_features = pdf_features
        self.tuples_to_check: list[tuple[PdfTag, PdfTag]] = list()

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

    def loop_tags(self):
        for page, tag in [(page, tag) for page in self.pdf_features.pages for tag in page.tags]:
            yield page, tag

    def get_modes(self):
        line_spaces, right_spaces = [0], [0]

        for page, tag in self.loop_tags():
            top, bottom = tag.bounding_box.top, tag.bounding_box.bottom
            left, right = tag.bounding_box.left, tag.bounding_box.right

            on_the_bottom = list(filter(lambda x: bottom < x.bounding_box.top, page.tags))
            same_line_tags = filter(
                lambda x: (top <= x.bounding_box.top < bottom) or (top < x.bounding_box.bottom <= bottom), page.tags
            )
            on_the_right = list(filter(lambda x: right < x.bounding_box.left, same_line_tags))

            if len(on_the_bottom):
                line_spaces.append(min(map(lambda x: int(x.bounding_box.top - bottom), on_the_bottom)))

            if not on_the_right:
                right_spaces.append(int(right))

        self.lines_space_mode = mode(line_spaces)
        self.right_space_mode = int(self.pdf_features.pages[0].page_width - mode(right_spaces))

    def get_mode_font(self):
        fonts_counter: Counter = Counter()
        for page, tag in self.loop_tags():
            fonts_counter.update([tag.font.font_id])

        if len(fonts_counter.most_common()) == 0:
            return

        font_mode_id = fonts_counter.most_common()[0][0]
        font_mode_tag = list(filter(lambda x: x.font_id == font_mode_id, self.pdf_features.fonts))
        if font_mode_tag:
            self.font_size_mode: float = float(font_mode_tag[0].font_size)

    def get_features(self, tag_1: PdfTag, tag_2: PdfTag, page_tags: list[PdfTag]):
        same_font = True if tag_1.font.font_id == tag_2.font.font_id else False

        return (
            [
                self.font_size_mode / 100,
                len(tag_1.content),
                len(tag_2.content),
                tag_1.content.count(" "),
                tag_2.content.count(" "),
                sum(character in string.punctuation for character in tag_1.content),
                sum(character in string.punctuation for character in tag_2.content),
            ]
            + self.get_position_features(tag_1, tag_2, page_tags)
            + [same_font]
            + self.get_first_letter_last_letter_one_hot_encoding(tag_1)
            + self.get_first_letter_last_letter_one_hot_encoding(tag_2)
        )

    def get_position_features(self, tag_1: PdfTag, tag_2: PdfTag, page_tags):
        top_1 = tag_1.bounding_box.top
        left_1, right_1 = tag_1.bounding_box.left, tag_1.bounding_box.right
        height_1, width_1 = tag_1.bounding_box.height, tag_1.bounding_box.width

        right_gap_1 = tag_1.on_the_right_left - right_1

        top_2 = tag_2.bounding_box.top
        left_2, right_2 = tag_2.bounding_box.left, tag_2.bounding_box.right
        height_2, width_2 = tag_2.bounding_box.height, tag_2.bounding_box.width

        left_gap_2 = left_2 - tag_2.on_the_left_right

        absolute_left_1 = min(left_1, left_1 if tag_1.on_the_left_left == 0 else tag_1.on_the_left_left)
        absolute_left_2 = min(left_2, left_2 if tag_2.on_the_left_left == 0 else tag_2.on_the_left_left)

        right_distance = left_2 - left_1 - width_1
        left_distance = left_1 - left_2

        height_difference = height_1 - height_2
        absolute_right_1 = max(left_1 + width_1, tag_1.on_the_right_right)
        absolute_right_2 = max(left_2 + width_2, tag_2.on_the_right_right)

        top_distance = top_2 - top_1 - height_1
        top_distance_gaps = self.get_top_distance_gap(tag_1, tag_2, page_tags)

        end_lines_difference = abs(absolute_right_1 - absolute_right_2)
        start_lines_differences = absolute_left_1 - absolute_left_2

        return [
            top_1,
            right_1,
            width_1,
            height_1,
            top_2,
            right_2,
            width_2,
            height_2,
            absolute_right_1,
            top_distance,
            top_distance - self.lines_space_mode,
            top_distance_gaps,
            top_distance - height_1,
            start_lines_differences,
            right_distance,
            left_distance,
            right_gap_1,
            left_gap_2,
            height_difference,
            end_lines_difference,
            self.lines_space_mode - top_distance_gaps,
            self.right_space_mode - absolute_right_1,
        ]

    @staticmethod
    def get_top_distance_gap(tag_1: PdfTag, tag_2: PdfTag, page_tags):
        top_distance = tag_2.bounding_box.top - tag_1.bounding_box.top - tag_1.bounding_box.height
        tags_in_the_middle = list(
            filter(lambda x: tag_1.bounding_box.bottom <= x.bounding_box.top < tag_2.bounding_box.top, page_tags)
        )
        tags_in_the_middle_top = (
            max(map(lambda x: x.bounding_box.top, tags_in_the_middle)) if len(tags_in_the_middle) > 0 else 0
        )
        tags_in_the_middle_bottom = (
            min(map(lambda x: x.bounding_box.bottom, tags_in_the_middle)) if len(tags_in_the_middle) > 0 else 0
        )
        gap_middle_top = (
            tags_in_the_middle_top - tag_1.bounding_box.top - tag_1.bounding_box.height if tags_in_the_middle_top > 0 else 0
        )
        gap_middle_bottom = tag_2.bounding_box.top - tags_in_the_middle_bottom if tags_in_the_middle_bottom > 0 else 0
        top_distance_gaps = top_distance - (gap_middle_bottom - gap_middle_top)
        return top_distance_gaps

    def get_left_right_block(self):
        for page, tag in self.loop_tags():
            left, right = tag.bounding_box.left, tag.bounding_box.right

            same_line_tags = self.get_same_line_tags(tag, page.tags)
            on_the_left = [each_tag for each_tag in same_line_tags if each_tag.bounding_box.right < right]

            tag.on_the_left_left = 0 if len(on_the_left) == 0 else min([x.bounding_box.left for x in on_the_left])
            tag.on_the_left_right = 0 if len(on_the_left) == 0 else max([x.bounding_box.right for x in on_the_left])

            on_the_right = [each_tag for each_tag in same_line_tags if left < each_tag.bounding_box.left]

            tag.on_the_right_left = 0 if len(on_the_right) == 0 else min(map(lambda x: x.bounding_box.left, on_the_right))
            tag.on_the_right_right = 0 if len(on_the_right) == 0 else max(map(lambda x: x.bounding_box.right, on_the_right))

    @staticmethod
    def get_same_line_tags(tag, tags):
        top, height = tag.bounding_box.top, tag.bounding_box.height

        same_line_tags = [
            each_tag
            for each_tag in tags
            if top <= each_tag.bounding_box.top < (top + height) or top < each_tag.bounding_box.bottom <= (top + height)
        ]

        return same_line_tags

    def get_first_letter_last_letter_one_hot_encoding(self, tag: PdfTag):
        tag_first_letter = [-1 if tag.id == "pad_tag" else 0] * self.len_letter_corpus
        tag_last_letter = [-1 if tag.id == "pad_tag" else 0] * self.len_letter_corpus

        if tag.content and tag.content[0] in self.letter_corpus.keys():
            tag_first_letter[self.letter_corpus[tag.content[0]]] = 1

        if tag.content and tag.content[-1] in self.letter_corpus.keys():
            tag_last_letter[self.letter_corpus[tag.content[-1]]] = 1

        return tag_first_letter + tag_last_letter

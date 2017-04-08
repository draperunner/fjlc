from enum import Enum
import re
from fjlc.utils.reader.line_reader import LineReader


TAB_REGEX = re.compile("\t")


class DataSetReader:

    def __init__(self, file_name, tweet_index, class_index):
        self.line_reader = LineReader(file_name)
        self.tweet_index = tweet_index
        self.class_index = class_index

    def has_next(self):
        return self.line_reader.has_next()

    def __next__(self):
        if not self.has_next():
            raise StopIteration
        return DataSetEntry(self.line_reader.__next__(), self.tweet_index, self.class_index)

    def __iter__(self):
        return self

    def get_progress(self):
        return self.line_reader.get_progress()


class DataSetEntry:

    def __init__(self, line, tweet_index, class_index):
        values = TAB_REGEX.split(line)
        self.tweet = values[tweet_index]
        self.classification = Classification.parse_classification_from_string(values[class_index])

    def get_tweet(self):
        return self.tweet

    def get_classification(self):
        return self.classification

    def apply_filters(self, filters):
        self.tweet = filters.apply(self.tweet)


class Classification(Enum):
    POSITIVE = 0
    NEUTRAL = 1
    NEGATIVE = 2

    @staticmethod
    def parse_classification_from_string(classification):
        if classification == "positive":
            return Classification.POSITIVE.name
        if classification == "neutral":
            return Classification.NEUTRAL.name
        if classification == "negative":
            return Classification.NEGATIVE.name

    @staticmethod
    def classify_from_thresholds(value, low_thresh, high_thresh):
        if value < low_thresh:
            return Classification.NEGATIVE.name
        elif value > high_thresh:
            return Classification.POSITIVE.name
        return Classification.NEUTRAL.name

    def is_positive(self):
        return self == Classification.POSITIVE

    def is_neutral(self):
        return self == Classification.NEUTRAL

    def is_negative(self):
        return self == Classification.NEGATIVE

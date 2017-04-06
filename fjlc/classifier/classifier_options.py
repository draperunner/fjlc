import copy
from enum import Enum

from fjlc.utils.file_utils import read_entire_file_into_string
from fjlc.utils.json_utils import from_json

options = {}
intensifiers = {}
negators = set()
stop_words = set()


def is_stop_word(word):
    return word in stop_words


def is_negation(word):
    return word in negators


def is_intensifier(word):
    return word in intensifiers


def contains_stop_words(words):
    for word in words:
        if is_stop_word(word):
            return True

    return False


def contains_negation(words):
    for word in words:
        if is_negation(word):
            return True

    return False


def contains_intensifier(words):
    for word in words:
        if is_intensifier(word):
            return True

    return False


def get_variable(variable):
    return options[variable.name]


def set_variable(variable, value):
    options[variable.name] = value


def get_options():
    return copy.deepcopy(options)


def is_special_class_word(word):
    return word.startswith("||") and word.endswith("||")


def load_options(file_name):
    """
    Loads options from a JSON file. The file should contain general classifier options, intensifier words with their
    intensification values, negation words and stop words.

    @param file_name Name of file containing the options
    @throws IOException
    """
    words = from_json(read_entire_file_into_string(file_name))

    global options, intensifiers, negators, stop_words
    options = words["options"]
    intensifiers = words["intensifiers"]
    negators = words["negators"]
    stop_words = words["stopWords"]


def get_intensifier_value(word):
    intensifier = intensifiers.get(word, 0.0)
    mult = get_variable(Variable.AMPLIFIER_SCALAR) if intensifier > 0 else get_variable(
        Variable.DOWNTONER_SCALAR)
    return mult * intensifier


class Variable(Enum):
    NEGATION_VALUE = 0,
    EXCLAMATION_INTENSIFIER = 1,
    QUESTION_INTENSIFIER = 2,
    NEGATION_SCOPE_LENGTH = 3,
    DOWNTONER_SCALAR = 4,
    AMPLIFIER_SCALAR = 5,
    CLASSIFICATION_THRESHOLD_LOWER = 6,
    CLASSIFICATION_THRESHOLD_HIGHER = 7

import sys
import fjlc.utils.file_utils as file_utils
import fjlc.utils.json_utils as json_utils
from fjlc.preprocessing.filters.filters import Filters

dictionary = {}


def load_dictionary(file_name):
    global dictionary
    dictionary = json_utils.from_json(file_utils.read_entire_file_into_string(file_name))


def correct_word_via_canonical(text):
    canonical = Filters.remove_repeating_characters(text)

    candidates = dictionary.get(canonical, None)
    if candidates is None:
        return text
    elif len(candidates) == 1:
        return candidates[0]

    closest_dist = sys.maxsize
    closest_string = canonical
    for candidate in candidates:
        dist = levenshtein_distance(text, candidate)
        if dist < closest_dist:
            closest_dist = dist
            closest_string = candidate

    return closest_string


def levenshtein_distance(s1, s2):
    """
    Calculates edit distance between two strings without replacement

    :param s1: String one
    :param s2: String two
    :return: Minimum number of insertions/deletions between the two strings to make them equal
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

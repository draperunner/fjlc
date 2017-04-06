import copy
from fjlc.utils.json_utils import from_json_file


class PriorPolarityLexicon:

    def __init__(self, polarity_lexicon):

        # Check if file name was given instead of ready polarity lexicon
        if type(polarity_lexicon) is str:
            self.polarity_lexicon = self.read_lexicon(polarity_lexicon)
        else:
            self.polarity_lexicon = polarity_lexicon

    def get_token_polarity(self, phrase):
        return self.polarity_lexicon[phrase]

    def has_token(self, word):
        return word in self.polarity_lexicon

    def get_subjective_words(self):
        return self.polarity_lexicon.keys()

    def get_lexicon(self):
        return copy.deepcopy(self.polarity_lexicon)

    @staticmethod
    def read_lexicon(file_name):
        return from_json_file(file_name)

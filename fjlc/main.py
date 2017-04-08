from os import path

import fjlc.classifier.classifier_options as classifier_options
import fjlc.lexical_classifier as lexical_classifier
import fjlc.preprocessing.filters.canonical_form as canonical_form
from fjlc.classifier.classifier import Classifier
from fjlc.lexicon.container.prior_polarity_lexicon import PriorPolarityLexicon
from fjlc.preprocessing.filters.filters import Filters
from fjlc.preprocessing.preprocessors.tweet_n_grams_pmi import TweetNGramsPMI
from fjlc.utils import json_utils, map_utils
from fjlc.lexicon.lexicon_creator import LexiconCreator
from fjlc.utils.reader.data_set_reader import DataSetReader
from fjlc.utils.reader.line_reader import LineReader

N_GRAM_STRING_FILTERS = [
    Filters.html_unescape, Filters.remove_unicode_emoticons, Filters.normalize_form, Filters.remove_url,
    Filters.remove_rt_tag, Filters.remove_hashtag, Filters.remove_username, Filters.remove_emoticons,
    Filters.remove_free_digits, str.lower
]
N_GRAM_CHARACTER_FILTERS = [
    Filters.remove_inner_word_characters, Filters.remove_non_syntactical_text, canonical_form.correct_word_via_canonical
]
N_GRAM_FILTERS = Filters(N_GRAM_STRING_FILTERS, N_GRAM_CHARACTER_FILTERS)

TWEET_STRING_FILTERS = [
    Filters.html_unescape, Filters.parse_unicode_emojis_to_alias, Filters.normalize_form, Filters.remove_url,
    Filters.remove_rt_tag, Filters.protect_hashtag, Filters.remove_email, Filters.remove_username,
    Filters.remove_free_digits, Filters.parse_emoticons, str.lower
]
TWEET_CHARACTER_FILTERS = [Filters.remove_inner_word_characters, Filters.remove_non_alphanumerical_text,
                           canonical_form.correct_word_via_canonical]
TWEET_FILTERS = Filters(TWEET_STRING_FILTERS, TWEET_CHARACTER_FILTERS)


class Lexicon:
    def __init__(self, n_grams_file, data_set_file, lexicon_file, max_error_rate, sentiment_value_threshold):
        self.n_grams_file = n_grams_file
        self.data_set_file = data_set_file
        self.lexicon_file = lexicon_file
        self.max_error_rate = max_error_rate
        self.sentiment_value_threshold = sentiment_value_threshold

    def create_lexicon(self):
        frequent_n_grams = json_utils.from_json_file(self.n_grams_file)
        data_set_reader = DataSetReader(self.data_set_file, 1, 0)

        lexicon_creator = LexiconCreator()
        # ProgressBar.track_progress(lexicon_creator, "Creating lexicon...")
        lexicon = lexicon_creator.create_lexicon(data_set_reader, frequent_n_grams, self.max_error_rate,
                                                 self.sentiment_value_threshold, TWEET_FILTERS)
        json_utils.to_json_file(self.lexicon_file, map_utils.sort_map_by_value(lexicon), True)

    @staticmethod
    def generate_n_grams(input_file, output_file, n_gram_range, cutoff_frequency, pmi_value_threshold):
        tweet_n_grams = TweetNGramsPMI()
        # ProgressBar.track_progress(tweet_n_grams, "Generating tweet n-grams...")
        ngrams = tweet_n_grams.get_frequent_n_grams(LineReader(input_file), n_gram_range, cutoff_frequency,
                                                    pmi_value_threshold, N_GRAM_FILTERS)

        json_utils.to_json_file(output_file, ngrams, True)


class LexiconClassifier:
    def __init__(self,
                 lexicon=path.join(path.abspath(path.dirname(__file__)), "res/data/lexicon.pmi.json"),
                 options=path.join(path.abspath(path.dirname(__file__)), "res/data/options.pmi.json"),
                 dictionary=path.join(path.abspath(path.dirname(__file__)), "res/dictionary.json")):
        self.lexicon = lexicon
        self.options = options
        self.dictionary = dictionary

        classifier_options.load_options(self.options)
        canonical_form.load_dictionary(self.dictionary)

        self.prior_polarity_lexicon = PriorPolarityLexicon(self.lexicon)
        self.classifier = Classifier(self.prior_polarity_lexicon, lexical_classifier.CLASSIFIER_FILTERS)

    def classify(self, tweets):
        """
        Classify tweet or tweets
        :param tweets: String or array of strings to classify.
        :return: String or array of strings depicting sentiment. Sentiment can be POSITIVE, NEGATIVE or NEUTRAL.
        """
        if type(tweets) == str:
            return self.classifier.classify(tweets)

        return list(map(lambda tweet: self.classifier.classify(tweet), tweets))

    def calculate_sentiment(self, tweets):
        """
        Classify tweet or tweets
        :param tweets: String or array of strings to classify.
        :return: Float or array of floats depicting sentiment value.
        """
        if type(tweets) == str:
            return self.classifier.calculate_sentiment(tweets)

        return list(map(lambda tweet: self.classifier.calculate_sentiment(tweet), tweets))

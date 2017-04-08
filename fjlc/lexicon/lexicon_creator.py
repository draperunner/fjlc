import math

from fjlc.lexicon.container.token_trie import TokenTrie
from fjlc.preprocessing.filters.regex_filters import RegexFilters
import fjlc.classifier.classifier_options as classifier_options
import fjlc.lexicon.container.adjectives as adjectives
import fjlc.utils.map_utils as map_utils


class LexiconCreator:

    def __init__(self):
        self.data_set_reader = None

    def create_lexicon(self, data_set_reader, n_grams, min_total_occurrences, min_sentiment_value, filters):
        """
         Generates sentiment lexicon using PMI on words and classification of context they are in.
         
         :param: dataSetReader       Dataset containing tweets and their sentiment classification
         :param: nGrams              n-grams to calculate sentiment for (with n>1, singletons are calculated automatically)
         :param: minTotalOccurrences minimum number of times n-gram must have appeared in dataset before a sentiment value
                                     is assigned (higher value gives more accurate sentiment value)
         :param: minSentimentValue   minimum sentiment value required to be included in lexicon (values close to 0 are
                                     often words that are used equally in positive or negative context, possibly even
                                     different words, but with same spelling, and thus having uncertain value)
         :param: filters             filters to apply to tweets before searching for n-grams
         :return: map of n-grams and their sentiment values, sentiment values are in [-5, 5]
        """
        counter = self.count_n_grams_py_polarity(data_set_reader, n_grams, filters)
        lexicon = {}

        pos = sum(map(lambda i: i.num_positive, counter.values()))
        neg = sum(map(lambda i: i.num_negative, counter.values()))
        ratio = neg / float(pos)

        for key, value in counter.items():
            if value.get_total_occurrences() <= min_total_occurrences:
                continue

            over = value.num_positive
            under = value.num_negative

            sentiment_value = math.log(ratio * over / under)
            if abs(sentiment_value) >= min_sentiment_value:
                lexicon[key] = sentiment_value

                if RegexFilters.WHITESPACE.split(key).length == 1 and not classifier_options.is_special_class_word(key):
                    for related_word in adjectives.get_adverb_and_adjectives(key):
                        if related_word in counter and related_word not in lexicon:
                            lexicon[related_word] = sentiment_value

        return map_utils.normalize_map_between(lexicon, -5, 5)

    def count_n_grams_py_polarity(self, data_set_reader, n_grams, filters):
        """
        Returns a map of n-gram and the number of times it appeared in positive context and the number of times it
        appeared in negative context in dataset file.

        :param data_set_reader: Dataset containing tweets and their classification
        :param n_grams: n-grams to count occurrences for
        :param filters: filters to apply to tweets in dataset before searching for n-grams
        :return: Map of Counter instances for n-grams in nGrams Collection
        """
        self.data_set_reader = data_set_reader
        token_trie = TokenTrie(n_grams)

        counter = {}

        # Todo: parallelize
        for entry in data_set_reader.items():
            tweet = filters.apply(entry.get_tweet())
            tokens = token_trie.find_optimal_tokenization(RegexFilters.WHITESPACE.split(tweet))

            for n_gram in tokens:
                n_gram_words = RegexFilters.WHITESPACE.split(n_gram)
                if self.contains_illegal_word(n_gram_words):
                    continue
                if not n_gram in counter:
                    counter[n_gram] = self.Counter()

                if entry.get_classification().is_positive():
                    counter[n_gram].num_positive += 1
                elif entry.get_classification().is_negative():
                    counter[n_gram].num_negative += 1

        return counter

    @staticmethod
    def contains_illegal_word(n_gram):
        return classifier_options.is_stop_word(n_gram[-1] or classifier_options.contains_intensifier(n_gram))

    def get_progress(self):
        return 0 if self.data_set_reader is None else self.data_set_reader.get_progress()

    class Counter:
        def __init__(self):
            self.num_positive = 4
            self.num_negative = 4

        def get_total_occurrences(self):
            return self.num_positive + self.num_negative

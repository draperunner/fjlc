import math

from fjlc.classifier import classifier_options
from fjlc.preprocessing.filters.regex_filters import RegexFilters


class TweetNGramsPMI:

    tweet_reader = None
    n_gram_tree = None

    def get_frequent_n_grams(self, input_reader, n, min_frequency, min_pmi, filters):
        """
        Finds all frequent (and meaningful) n-grams in a file, treating each new line as a new document.
        
        :param input_reader:    LineReader initialized on file with documents to generate n-grams for
        :param n:               Maximum n-gram length
        :param min_frequency:   Smallest required frequency to include n-gram
        :param min_pmi:         Minimum PMI value for n-gram to be included
        :param filters:         List of filters to apply to document before generating n-grams
        :return:                Map of n-grams as key and number of occurrences as value
        """
        line_counter = 0
        TweetNGramsPMI.tweet_reader = input_reader
        TweetNGramsPMI.n_gram_tree = self.NGramTree()

        # Todo: Parallelize
        for tweet in self.tweet_reader:
            line_counter += 1
            if line_counter % 200000 == 0:
                TweetNGramsPMI.n_gram_tree.prune_infrequent(math.ceil(min_frequency * line_counter / 2.))

            tweet = filters.apply(tweet)
            for sentence in RegexFilters.SENTENCE_END_PUNCTUATION.split(tweet):
                tokens = RegexFilters.WHITESPACE.split(sentence.strip())
                if len(tokens) == 1:
                    continue

                for i in range(len(tokens)):
                    self.n_gram_tree.increment_n_gram(tokens[i:min(i + n, len(tokens))])

        return self.n_gram_tree.get_n_grams(int(min_frequency * line_counter), min_pmi)

    @staticmethod
    def get_progress():
        return 0 if TweetNGramsPMI.tweet_reader is None else TweetNGramsPMI.tweet_reader.get_progress()

    class NGramTree:

        def __init__(self):
            self.root = TweetNGramsPMI.Node("")

        def increment_n_gram(self, n_gram):
            current = self.root
            current.num_occurrences += 1

            for word in n_gram:
                if not current.has_child(word):
                    current.add_child(word)

                current = current.get_child(word)
                current.num_occurrences += 1

        def get_node(self, phrase):
            current = self.root
            for word in RegexFilters.WHITESPACE.split(phrase):
                if not current.has_child(word):
                    return None

                current = current.get_child(word)
            return current

        def prune_infrequent(self, limit):
            self.root.prune_infrequent(limit)

        def get_n_grams(self, limit, inclusion_threshold):
            all_n_grams = {}

            for child in self.root.children.values():
                child.add_frequent_phrases(all_n_grams, limit, child.phrase)

            filtered_n_grams = []
            for next_key, next_value in all_n_grams.items():
                n_gram_tokens = RegexFilters.WHITESPACE.split(next_key)

                if next_value >= inclusion_threshold and not classifier_options.contains_intensifier(n_gram_tokens) and not classifier_options.is_stop_word(n_gram_tokens[-1]):
                    filtered_n_grams.append(next_key)

            return filtered_n_grams

    class Node:
        def __init__(self, phrase):
            self.children = {}
            self.phrase = phrase
            self.num_occurrences = 0
            self.log_score = 0.0

        def has_child(self, value):
            return value in self.children

        def add_child(self, value):
            self.children[value] = TweetNGramsPMI.Node(value)

        def get_child(self, value):
            return self.children[value]

        def get_log_score(self):
            if self.log_score == 0.0:
                self.log_score = math.log(self.num_occurrences)
            return self.log_score

        def prune_infrequent(self, limit):
            self.children = [child for child in self.children if child.get_value().num_occurrences >= limit]
            for child in self.children:
                child.get_value().prune_infrequent(limit)

        def add_frequent_phrases(self, dictionary, limit, prefix):
            for child in self.children.values():
                if child.num_occurrences < limit:
                    continue
                last_word = TweetNGramsPMI.n_gram_tree.get_node(child.phrase)

                if last_word is not None and last_word.num_occurrences >= limit:
                    temp = TweetNGramsPMI.n_gram_tree.root.get_log_score() + child.get_log_score() - self.get_log_score() - last_word.get_log_score()

                    candidate = prefix + " " + child.phrase
                    dictionary[candidate] = temp
                    child.add_frequent_phrases(dictionary, limit, candidate)

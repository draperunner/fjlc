from fjlc.preprocessing.filters.regex_filters import RegexFilters
import fjlc.classifier.classifier_options as classifier_options
import functools


class TokenTrie:

    def __init__(self, sentences):
        """
        Creates a phrase trie for efficient sub-phrase look up

        @param sentences List of Strings of all the phrases which are whitespace delimited n-grams
        """
        self.root = TokenTrie.Node()
        for sentence in sentences:
            words = RegexFilters.WHITESPACE.split(sentence)
            self.add_token_sequence(words)

    def add_token_sequence(self, token_sequence):
        tree = self.root
        for token in token_sequence:
            if not tree.has_child(token):
                tree.add_child(token)
            tree = tree.get_child(token)
        tree.set_phrase_end(True)

    def has_tokens(self, phrase):
        """
        Checks if phrase or sub-phrase exists in the tree.

        If set of phrases contains phrases such as: "state", "of the" and "state of the art", look up on:
        "state" returns true, "of" returns null, "of the art" returns false.

        :param phrase: Phrase or sub-phrase to look up.
        :type: phrase: list of str
        :return: Returns true if phrase in its entirety is in the tree,
        null if part of the phrase matches a larger tokenSequence,
        false if phrases matches no other phrase entirely and not part any longer phrase.
        """

        if len(phrase) == 1 and classifier_options.is_special_class_word(phrase[0]):
            return True

        tree = self.root
        for token in phrase:
            if not tree.has_child(token):
                return False
            tree = tree.get_child(token)

        return True if tree.is_end_of_phrase() else None

    def find_tracked_words(self, tokens):
        """
        Finds word-ranges all of phrases in tokens stored in TokenTrie

        :param tokens: Sequence of tokens to find phrases in
        :type tokens: list of str
        :return: List of Tokens found in tokens
        """
        tracked_words = []

        for i in range(len(tokens)):
            for j in range(i + 1, len(tokens) + 1):
                phrase = tokens[i:j]
                status = self.has_tokens(phrase)

                if status is not None:
                    if status is True:
                        tracked_words.append(TokenTrie.Token(phrase, i, j - 1))
                    elif status is False:
                        break

        return tracked_words

    def find_optimal_allocation(self, tokens):
        """
        Finds longest, non-overlapping word-ranges of phrases in tokens stored in TokenTrie

        :param tokens: tokens tokenize
        :type tokens: list of str
        :return: Optimal allocation of tokens to phrases
        :rtype: list of TokenTrie.Token
        """
        token_ranges = self.find_tracked_words(tokens)
        token_ranges.sort()

        for offset in range(1, len(token_ranges)):
            to_be_removed = []
            for candidate in token_ranges[offset:]:
                for i in range(offset):
                    if token_ranges[i].overlaps_with(candidate):
                        to_be_removed.append(candidate)
                        break

            token_ranges = [token for token in token_ranges if token not in to_be_removed]

        token_ranges.sort(key=lambda token: token.get_start_index())
        return token_ranges

    def find_optimal_tokenization(self, tokens):
        """
        Similar to {@link #findOptimalAllocation(String[])}, but also includes the words not matching any longer n-gram
        in TokenTrie as singletons.

        :param tokens: tokens to tokenize
        :return: Optimal allocation of tokens to phrases, with non matching tokens as singletons.
        """
        token_ranges = self.find_optimal_allocation(tokens)
        tokenized_sentence = []

        set_index = 0
        for token in token_ranges:
            while set_index < token.get_start_index():
                tokenized_sentence.append(tokens[set_index])
                set_index += 1
            tokenized_sentence.append(" ".join(token.get_token_sequence()))
            set_index = token.get_end_index() + 1

        while set_index < len(tokens):
            tokenized_sentence.append(tokens[set_index])
            set_index += 1

        return tokenized_sentence

    @functools.total_ordering
    class Token:

        def __init__(self, token_sequence, start_index, end_index):
            self.token_sequence = token_sequence
            self.start_index = start_index
            self.end_index = end_index

        def get_token_sequence(self):
            return self.token_sequence

        def get_start_index(self):
            return self.start_index

        def get_end_index(self):
            return self.end_index

        def get_phrase_length(self):
            return self.end_index - self.start_index

        def overlaps_with(self, other):
            """
            Checks if two phrases overlap
            :param other: The other token_sequence
            :return: True if overlap, False otherwise
            """
            return self.get_start_index() <= other.get_end_index() and other.get_start_index() <= self.get_end_index()

        def __lt__(self, other):
            size_diff = other.get_phrase_length() - self.get_phrase_length()
            diff = size_diff if size_diff != 0 else other.get_start_index() - self.get_start_index()
            return diff < 0

        def __eq__(self, other):
            size_diff = other.get_phrase_length() - self.get_phrase_length()
            diff = size_diff if size_diff != 0 else other.get_start_index() - self.get_start_index()
            return diff == 0

        def __str__(self):
            return str(self.token_sequence)

        def __repr__(self):
            return "Token(" + str(self.start_index) + "," + str(self.end_index) + ")<" + str(self.token_sequence) + ">"

    class Node:

        def __init__(self):
            self.children = {}
            self.end_of_phrase = False

        def has_child(self, value):
            return value in self.children

        def add_child(self, value):
            self.children[value] = TokenTrie.Node()

        def get_child(self, value):
            return self.children[value]

        def set_phrase_end(self, phrase_end):
            self.end_of_phrase = phrase_end

        def is_end_of_phrase(self):
            return self.end_of_phrase

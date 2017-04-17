import unittest

from fjlc.lexicon.container.prior_polarity_lexicon import PriorPolarityLexicon
from fjlc.lexicon.container.token_trie import TokenTrie
from os import path


class TokenTest(unittest.TestCase):

    def setUp(self):
        lexicon = path.join(path.abspath(path.dirname(__file__)), "../res/data/lexicon.pmi.json")
        prior_polarity_lexicon = PriorPolarityLexicon(lexicon)
        self.phrase_tree = TokenTrie(prior_polarity_lexicon.get_subjective_words())
        self.tweet = "you have a great day"

    def test_has_tokens(self):
        """
        Checks if phrase or sub-phrase exists in the tree. If set of phrases contains phrases such as: "state", "of the"
        and "state of the art", look up on:
        "state" returns true, "of" returns null, "of the art" returns false.
        """
        trie = TokenTrie(["state", "of the", "state of the art"])

        self.assertTrue(trie.has_tokens(["state"]))
        self.assertIsNone(trie.has_tokens(["of"]))
        self.assertFalse(trie.has_tokens(["of", "the", "art"]))

    def test_optimal_allocation(self):
        optimal = self.phrase_tree.find_optimal_allocation(self.tweet.split(" "))
        self.assertEqual([self.tweet.split(" ")], list(map(lambda token: token.token_sequence, optimal)))


if __name__ == '__main__':
    unittest.main()

import unittest

from fjlc.main import LexiconClassifier


class ClassificationTest(unittest.TestCase):

    def setUp(self):
        self.classifier = LexiconClassifier()
        self.most_positive = "you have a great day"
        self.most_positive_intensified = "you have a very great day"
        self.most_negative = "a bad bitch"
        self.most_negative_intensified = "a very bad bitch"

    def test_sentiment_of_exact_lexicon_tokens(self):
        self.assertEqual(5.0, self.classifier.calculate_sentiment(self.most_positive))
        self.assertEqual(-5.0, self.classifier.calculate_sentiment(self.most_negative))

    def test_intensification(self):
        normal = self.classifier.calculate_sentiment(self.most_positive)
        intensified = self.classifier.calculate_sentiment(self.most_positive_intensified)
        self.assertGreater(intensified, normal)

        normal_neg = self.classifier.calculate_sentiment(self.most_negative)
        intensified_neg = self.classifier.calculate_sentiment(self.most_negative_intensified)
        self.assertLess(intensified_neg, normal_neg)

    def test_exclamation_mark(self):
        normal = self.classifier.calculate_sentiment(self.most_positive)
        with_exclamation = self.classifier.calculate_sentiment(self.most_positive + "!")
        self.assertGreater(with_exclamation, normal)

        intensified_normal = self.classifier.calculate_sentiment(self.most_positive_intensified)
        intensified_with_exclamation = self.classifier.calculate_sentiment(self.most_positive_intensified + "!")
        self.assertGreater(intensified_with_exclamation, intensified_normal)

if __name__ == '__main__':
    unittest.main()

import fjlc.classifier.classifier_options as classifier_options
import fjlc.classifier.sentence.lexical_parser as lexical_parser
from fjlc.lexicon.container.token_trie import TokenTrie
from fjlc.utils.reader.data_set_reader import Classification


def propagate_negation(lexical_tokens, index):
    negation_scope_length = classifier_options.get_variable(classifier_options.Variable.NEGATION_SCOPE_LENGTH)
    for i in range(index + 1, int(min(index + negation_scope_length, len(lexical_tokens)))):
        lexical_tokens[i].set_in_negated_context(True)
        if lexical_tokens[i].is_at_the_end_of_sentence():
            break


def intensify_next(lexical_tokens, index, intensification):
    if not lexical_tokens[index].is_at_the_end_of_sentence():
        lexical_tokens[index + 1].intensify_token(intensification)


class Classifier:
    def __init__(self, lexicon, filters=None):
        self.lexicon = lexicon
        self.filters = filters
        self.phrase_tree = TokenTrie(lexicon.get_subjective_words())

    def classify(self, tweet):
        """
        Classifies the tweet into one of three classes (negative, neutral or positive) depending on the sentiment value
        of the tweet and the thresholds specified in the classifier_options

        :param tweet: String tweet to classify
        :return: Sentiment classification (negative, neutral or positive)
        """
        sentiment_value = self.calculate_sentiment(tweet)

        return Classification.classify_from_thresholds(sentiment_value,
                                                       classifier_options.get_variable(
                                                           classifier_options.Variable.CLASSIFICATION_THRESHOLD_LOWER),
                                                       classifier_options.get_variable(
                                                           classifier_options.Variable.CLASSIFICATION_THRESHOLD_HIGHER))

    def calculate_sentiment(self, tweet):
        if self.filters is not None:
            tweet = self.filters.apply(tweet)

        lexical_tokens = lexical_parser.lexically_parse_tweet(tweet, self.phrase_tree)
        for i in range(len(lexical_tokens)):
            token = lexical_tokens[i]
            phrase = token.get_phrase()

            if self.lexicon.has_token(phrase):
                token.set_lexical_value(self.lexicon.get_token_polarity(phrase))

            elif classifier_options.is_negation(phrase):
                propagate_negation(lexical_tokens, i)

            elif classifier_options.is_intensifier(phrase):
                intensify_next(lexical_tokens, i, classifier_options.get_intensifier_value(phrase))

        return sum(map(lambda t: t.get_sentiment_value(), lexical_tokens))

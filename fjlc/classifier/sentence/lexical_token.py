import fjlc.classifier.classifier_options as classifier_options


class LexicalToken:
    def __init__(self, phrase):
        self.phrase = phrase
        self.lexical_value = 0.0
        self.intensification = 1

        self.in_negated_context = False
        self.at_end_of_sentence = False

    def get_phrase(self):
        return self.phrase

    def set_lexical_value(self, lexical_value):
        self.lexical_value = lexical_value

    def get_sentiment_value(self):
        sentiment_value = self.lexical_value
        if self.is_under_intensification():
            sentiment_value *= self.intensification

        if self.is_in_negated_context() and sentiment_value != 0:
            negation_value = classifier_options.get_variable(classifier_options.Variable.NEGATION_VALUE)
            sentiment_value = sentiment_value - negation_value if sentiment_value > 0 else sentiment_value + negation_value

        return sentiment_value

    def set_in_negated_context(self, in_negated_context):
        self.in_negated_context = in_negated_context

    def is_in_negated_context(self):
        return self.in_negated_context

    def set_at_end_of_sentence(self, at_end_of_sentence):
        self.at_end_of_sentence = at_end_of_sentence

    def is_at_the_end_of_sentence(self):
        return self.at_end_of_sentence

    def intensify_token(self, intensification):
        self.intensification *= intensification

    def is_under_intensification(self):
        return self.intensification != 1

    def __str__(self):
        return "[" + self.phrase + (
            "_NEG" if self.is_in_negated_context() else "") + " | " + str(self.get_sentiment_value()) + " | " + str(
            self.intensification) + "]"

    def __repr__(self):
        return self.__str__()

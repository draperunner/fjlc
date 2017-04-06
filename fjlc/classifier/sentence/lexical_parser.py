"""
import com.freva.masteroppgave.lexicon.container.TokenTrie;
"""

import fjlc.classifier.classifier_options as classifier_options
from fjlc.classifier.sentence.lexical_token import LexicalToken
from fjlc.preprocessing.filters.regex_filters import RegexFilters


def lexically_parse_tweet(tweet, phrase_tree):
    """
    Returns list of LexicalTokens found in tweet. The list contains all the words in original tweet, but are
    optimally grouped up to form largest matching n-grams from lexicon. If no match is found, token is added as
    singleton.

    @param tweet      Tweet to lexically parse
    @param phrase_tree Token tree that contains all the lexical n-grams
    @return List of LexicalTokens
    """
    lexical_tokens = []

    prev = 0

    while True:
        match = RegexFilters.SENTENCE_END_PUNCTUATION.search(tweet[prev:])
        if match is None:
            break
        span = match.span()
        sentence = tweet[prev:prev + span[0]]
        punctuation = match.group(0)
        prev += span[1]
        lexical_tokens.extend(parse_sentence(sentence, punctuation, phrase_tree))

    lexical_tokens.extend(parse_sentence(tweet[prev:], None, phrase_tree))

    return lexical_tokens


def parse_sentence(sentence, punctuation, phrase_tree):
    sentence_tokens = RegexFilters.WHITESPACE.split(sentence)

    tokenized_sentence = phrase_tree.find_optimal_tokenization(sentence_tokens)
    tokens = list(map(lambda s: LexicalToken(s), tokenized_sentence))

    if len(tokens) > 0:
        tokens[len(tokens) - 1].set_at_end_of_sentence(True)

        if punctuation is not None and "!" in punctuation:
            exclamation_intensifier = classifier_options.get_variable(classifier_options.Variable.EXCLAMATION_INTENSIFIER)
            for token in tokens:
                token.intensify_token(exclamation_intensifier)

        elif punctuation is not None and "?" in punctuation:
            question_intensifier = classifier_options.get_variable(classifier_options.Variable.QUESTION_INTENSIFIER)
            for token in tokens:
                token.intensify_token(question_intensifier)

    return tokens

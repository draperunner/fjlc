import html
import re
import fjlc.classifier.classifier_options as classifier_options
from fjlc.preprocessing.filters.regex_filters import RegexFilters
from normalizr import Normalizr

normalizr = Normalizr(language="en")


class Filters:
    USERNAME_PLACEHOLDER = " ||username|| "
    HASHTAG_PLACEHOLDER = " ||hashtag|| "
    RTTAG_PLACEHOLDER = " ||rt|| "
    URL_PLACEHOLDER = " ||url|| "

    def __init__(self, string_filters, token_filters):
        self.string_filters = string_filters
        self.token_filters = token_filters

    def apply(self, text):
        text = self.string_chain(text, self.string_filters)
        return self.token_chain(text, self.token_filters).strip()

    @staticmethod
    def string_chain(text, filters):
        """
        Chain several filters after each other, applies the filter on the entire string
        :param text: String to format
        :param filters: Sequence of filters to apply on String
        :return: The formatted String
        """
        if filters is None:
            return text

        for filter_function in filters:
            text = filter_function(text)

        return text

    @staticmethod
    def token_chain(text, filters):
        """
        Chain several filters after each other, applying filters only on non special class tokens as detected by
        {@link ClassifierOptions#isSpecialClassWord(String)}

        :param text: String to format
        :param filters: Sequence of filters to apply to tokens
        :return: The formatted String
        """
        if filters is None:
            return text

        sb = ""
        for token in RegexFilters.WHITESPACE.split(text):
            if not classifier_options.is_special_class_word(token):
                token = Filters.string_chain(token, filters)

            sb += token + " "

        return sb

    @staticmethod
    def html_unescape(text):
        """
        Returns HTML unescaped string

        :param text: String to format (f.ex. "&lt;3")
        :return: The formatted String (f.ex. "<3")
        """
        return html.unescape(text)

    @staticmethod
    def normalize_form(text):
        """
        Normalizes String to Latin characters if possible. WARNING: This also applies non-ASCII filter to the entire string

        :param text: String to format (f.ex. "A strîng wìth fúnny chäracters")
        :return: The formatted String (f.ex. "A string with funny characters")
        """
        return normalizr.remove_accent_marks(text)

    @staticmethod
    def remove_repeated_whitespace(text):
        """
        Removes repeated whitespace

        :param text: String to format (f.ex. "A string    with maany   spaces  ")
        :return: The formatted String (f.ex. "A string with many spaces ")
        """
        return RegexFilters.replace_whitespace(text, " ")

    @staticmethod
    def parse_unicode_emojis_to_alias(text):
        """
        Uses {@link EmojiParser#parseFromUnicode(String, EmojiParser.EmojiTransformer)} to parse unicode emojis to ASCII
        string " ||emoji_alias|| ".

        :param text: String to format (f.ex. "Hey \uD83D\uDC66\uD83C\uDFFF!")
        :return: The formatted String (f.ex. "Hey  ||boy|| !")
        """
        #return EmojiParser.parseFromUnicode(text, EMOJI_ALIAS_TRANSFORMER)
        return text

    @staticmethod
    def remove_unicode_emoticons(text):
        return normalizr.replace_emojis(text)

    @staticmethod
    def parse_emoticons(text):
        return RegexFilters.replace_emoticons(text, " ||$1|| ")

    @staticmethod
    def remove_emoticons(text):
        return RegexFilters.replace_emoticons(text, "")

    @staticmethod
    def remove_username(text):
        return RegexFilters.replace_username(text, "")

    @staticmethod
    def placeholder_username(text):
        return RegexFilters.replace_username(text, Filters.USERNAME_PLACEHOLDER)

    @staticmethod
    def remove_email(text):
        return re.sub(RegexFilters.TWITTER_EMAIL, "", text)

    @staticmethod
    def remove_hashtag(text):
        return RegexFilters.replace_hashtag(text, "")

    @staticmethod
    def placeholder_hashtag(text):
        return RegexFilters.replace_hashtag(text, Filters.HASHTAG_PLACEHOLDER)

    @staticmethod
    def hashtag_to_word(text):
        return RegexFilters.replace_hashtag(text, "$1")

    @staticmethod
    def protect_hashtag(text):
        return RegexFilters.replace_hashtag(text, " ||#$1|| ")

    @staticmethod
    def remove_rt_tag(text):
        return RegexFilters.replace_rt_tag(text, "")

    @staticmethod
    def placeholder_rt_tag(text):
        return RegexFilters.replace_rt_tag(text, Filters.RTTAG_PLACEHOLDER)

    @staticmethod
    def remove_url(text):
        return RegexFilters.replace_url(text, "")

    @staticmethod
    def placeholder_url(text):
        return RegexFilters.replace_url(text, Filters.URL_PLACEHOLDER)

    @staticmethod
    def remove_inner_word_characters(text):
        """
        Removes characters which are often part of a word (mostly apostrophes)

        :param text: String to format (f.ex. "Here's a sentence!")
        :return: The formatted String (f.ex. "Heres a sentence!")
        """
        return RegexFilters.replace_inner_word_characters(text, "")

    @staticmethod
    def remove_non_syntactical_text(text):
        """
        Removes all non-alphabetic or basic punctuation characters (!?,. )

        :param text: String to format (f.ex. "This is' a #crazy tæst")
        :return: The formatted String (f.ex. "This is a crazy tst")
        """
        return RegexFilters.replace_non_syntactical_text(text, " ")

    @staticmethod
    def remove_non_syntactical_text_plus(text):
        return RegexFilters.replace_non_syntactical_text_plus(text, " ")

    @staticmethod
    def remove_non_alphanumerical_text(text):
        """
        Removes non-alphanumerical characters

        :param text: String to format (f.ex "It's very nice!")
        :return: The formatted String (f.ex "It s very nice ")
        """
        return RegexFilters.replace_non_alphanumerical_text(text, " ")

    @staticmethod
    def remove_non_alphabetic_text(text):
        """
        Removes non alphabetic characters

        :param text: String to format (f.ex "Hey, m8!")
        :return: The formatted String (f.ex. "Hey m")
        """
        return RegexFilters.replace_non_alphabetic_text(text, "")

    @staticmethod
    def remove_free_digits(text):
        """
        Removes free standing digits (digits not part of a word)

        :param text: String to format (f.ex. "Only 90s kids will get this 1337 m8")
        :return: The formatted String (f.ex. "Only 90s kids will get this m8")
        """
        return RegexFilters.replace_free_digits(text, " ")

    @staticmethod
    def remove_repeating_characters(text):
        """
        Replaces repeating characters in String

        :param text: String to format (f.ex. "Today is a greeeeeeaaaaaaat dayy!")
        :return: The formatted String (f.ex. "Today is a great day!")
        """
        return RegexFilters.replace_repeating_characters(text, "$1")

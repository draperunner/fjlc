import re

# Emoticon definitions.
NormalEyes = "[:=8]"
WinkEyes = "[;]"
NoseArea = "[Ooc^*'-]?"
HappyMouths = "[)*>}\\]]"
SadMouths = "[c<|@L{/\\(\\[]"
conditionalEmotes = "([x=;:]" + NoseArea + "d|[=;:]p)"


class RegexFilters:
    EMOTICON_NEGATIVE = re.compile("(" + NormalEyes + NoseArea + SadMouths + ")")
    EMOTICON_POSITIVE = re.compile("(\\^_\\^|<3+|" + "((" + NormalEyes + "|" +
                                   WinkEyes + ")" + NoseArea + HappyMouths + "))")
    EMOTICON_CONDITIONAL_LEFT = re.compile("(?:(?:^|\\s)" + conditionalEmotes + ")", re.IGNORECASE)
    EMOTICON_CONDITIONAL_RIGHT = re.compile("(?:" + conditionalEmotes + "(?:$|\\s))", re.IGNORECASE)

    # Twitter basic elements
    TWITTER_USERNAME = re.compile("(@\\w{1,15})")
    TWITTER_HASHTAG = re.compile("#([a-zA-Z]+\\w*)")
    TWITTER_RT_TAG = re.compile("(^RT\\s+|\\s+RT\\s+)")
    TWITTER_URL = re.compile("((https?://|www)\\S+)")
    TWITTER_EMAIL = re.compile("\\w+@\\S+")

    WHITESPACE = re.compile("\\s+")
    INNER_WORD_CHAR = re.compile("['`´’]")
    NON_SYNTACTICAL_TEXT = re.compile("[^a-z ?!.,]", re.IGNORECASE)
    NON_SYNTACTICAL_TEXT_PLUS = re.compile("[^a-z ?!.]", re.IGNORECASE)
    SENTENCE_END_PUNCTUATION = re.compile("[!?,.]")

    NON_ALPHANUMERIC_TEXT = re.compile("[^a-zA-Z0-9 ]")
    NON_ALPHABETIC_TEXT = re.compile("[^a-zA-Z ]")
    NON_ASCII_CHARACTERS = re.compile("[^\\p{ASCII}]")
    FREE_DIGITS = re.compile("([^\\w]|^)[0-9]+([^\\w]+[0-9]+)*([^\\w]|$)")
    REPEATING_CHARACTERS = re.compile("(.)\\1+")

    @staticmethod
    def replace_emoticons(text, replace):
        new_text = re.sub(RegexFilters.EMOTICON_POSITIVE, replace, text)
        new_text = re.sub(RegexFilters.EMOTICON_NEGATIVE, replace, new_text)
        new_text = re.sub(RegexFilters.EMOTICON_CONDITIONAL_LEFT, replace, new_text)
        return re.sub(RegexFilters.EMOTICON_CONDITIONAL_RIGHT, replace, new_text)

    @staticmethod
    def replace_username(text, replace):
        return re.sub(RegexFilters.TWITTER_USERNAME, replace, text)

    @staticmethod
    def replace_hashtag(text, replace):
        return re.sub(RegexFilters.TWITTER_HASHTAG, replace, text)

    @staticmethod
    def replace_rt_tag(text, replace):
        return re.sub(RegexFilters.TWITTER_RT_TAG, replace, text)

    @staticmethod
    def replace_url(text, replace):
        return re.sub(RegexFilters.TWITTER_URL, replace, text)

    @staticmethod
    def replace_whitespace(text, replace):
        return re.sub(RegexFilters.WHITESPACE, replace, text)

    @staticmethod
    def replace_inner_word_characters(text, replace):
        return re.sub(RegexFilters.INNER_WORD_CHAR, replace, text)

    @staticmethod
    def replace_non_syntactical_text(text, replace):
        return re.sub(RegexFilters.NON_SYNTACTICAL_TEXT, replace, text)

    @staticmethod
    def replace_non_syntactical_text_plus(text, replace):
        return re.sub(RegexFilters.NON_SYNTACTICAL_TEXT_PLUS, replace, text)

    @staticmethod
    def replace_non_alphanumerical_text(text, replace):
        return re.sub(RegexFilters.NON_ALPHANUMERIC_TEXT, replace, text)

    @staticmethod
    def replace_non_alphabetic_text(text, replace):
        return re.sub(RegexFilters.NON_ALPHABETIC_TEXT, replace, text)

    @staticmethod
    def replace_free_digits(text, replace):
        return re.sub(RegexFilters.FREE_DIGITS, replace, text)

    @staticmethod
    def replace_non_ascii(text, replace):
        return re.sub(RegexFilters.NON_ASCII_CHARACTERS, replace, text)

    @staticmethod
    def replace_repeating_characters(text, replace):
        return re.sub(RegexFilters.REPEATING_CHARACTERS, replace, text)

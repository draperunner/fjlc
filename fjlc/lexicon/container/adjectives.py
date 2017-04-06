VOWELS = "aeiouy"
SEPARATOR = ","


def get_adverb_and_adjectives(word):
    if not consists_only_of_alphabetical_characters(word):
        return []

    adjectives = get_comparative_and_superlative_adjectives(word)
    if len(adjectives) == 0:
        return [form_adverb_from_adjective(word)]
    else:
        adjectives = form_adverb_from_adjective(word) + SEPARATOR + adjectives
        return adjectives.split(SEPARATOR)


def get_comparative_and_superlative_adjectives(word):
    """
    Returns a comma separated string with the comparative and the superlative forms of the input adjective. F.ex.
    "good" => "better,best", "happy" => "happier,happiest". If the comparative and superlative forms are
    "more [word]" and "most [word]", empty string is returned, f.ex. "careful" => "".
    Forms are generated using rules from: http://www.eflnet.com/tutorials/adjcompsup.php

    :param word: adjective
    :return: comma separated comparative and the superlative forms of the input adjective
    """
    if word == "good":
        return "better,best"
    if word == "bad":
        return "worse,worst"
    if word == "far":
        return "farther,farthest"
    if word == "little":
        return "less,least"
    if word == "slow":
        return "slower,slowest"

    return normal_comparative_and_superlative_adjectives(word)


def normal_comparative_and_superlative_adjectives(word):
    number_of_syllables = get_number_of_syllables(word)
    sb = ""

    if number_of_syllables == 1: # If one-syllable adjective
        last_letter = word[-1]

        # If the adjective ends with an e, just add –r for the comparative form and –st for the superlative form
        if word.endswith("e"):
            sb += word + "r"
            sb += SEPARATOR + word + "st"

        # If the adjective ends with –y, change the y to i and add –er for the comparative form.
        # For the superlative form change the y to i and add –est.
        elif word.endswith("y"):
            stub = word[:-1]
            sb += stub + "ier"
            sb += SEPARATOR + stub + "iest"

        # If the adjective ends with a single consonant with a vowel before it, double the consonant and add –er
        # for the comparative form; and double the consonant and add –est for the superlative form
        elif is_vowel(word[-2]) and not is_vowel(last_letter):
            sb += word + last_letter + "er"
            sb += SEPARATOR + word + last_letter + "est"

        # Otherwise just add -er for the comparative form and -est for the superlative form
        else:
            sb += word + "er"
            sb += SEPARATOR + word + "est"

    elif number_of_syllables == 2: # If two-syllable adjective
        # If the adjective ends with –y, change the y to i and add –er for the comparative form.
        # For the superlative form change the y to i and add –est.
        if word.endswith("y"):
            stub = word[:-1]
            sb += stub + "ier"
            sb += SEPARATOR + stub + "iest"

        # If the adjective ending in –er, -le, or –ow, add –er and –est to form the comparative and superlative forms
        elif word.endswith("er") or word.endswith("le") or word.endswith("ow"):
            sb += word + "er"
            sb += SEPARATOR + word + "est"

    return sb


def form_adverb_from_adjective(adjective):
    """
    Forms an adverb from the input adjective, f.ex. "happy" => "happily".
    Adverbs are generated using rules from: http://www.edufind.com/english-grammar/forming-adverbs-adjectives/

    :param adjective: adjective
    :return: adverb form of the input adjective
    """

    # If the adjective ends in -able, -ible, or -le, replace the -e with -y
    if adjective.endswith("able") or adjective.endswith("ible") or adjective.endswith("le"):
        return adjective[:-1] + "y"

    # If the adjective ends in -y, replace the y with i and add -ly
    elif adjective.endswith("y"):
        return adjective[:-1] + "ily"

    # If the adjective ends in -ic, add -ally
    elif adjective.endswith("ic"):
        return adjective[:-2] + "ally"

    # In most cases, an adverb is formed by adding -ly to an adjective
    return adjective + "ly"


def get_number_of_syllables(word):
    count = 0
    last_is_consonant = True

    for i in range(len(word) - 1):
        if is_vowel(word[i]):
            if last_is_consonant:
                count += 1
            last_is_consonant = False
        else:
            last_is_consonant = True

    return count


def is_vowel(character):
    return character in VOWELS


def consists_only_of_alphabetical_characters(name):
    return name.isalpha()

import pronouncing


def get_arpabet(word):
    """
    Get the first CMU pronunciation
    for an English word.
    """

    pronunciations = pronouncing.phones_for_word(
        word.lower()
    )

    if pronunciations:
        return pronunciations[0]

    return None


def get_all_pronunciations(word):
    """
    Return all available pronunciations
    for a word.
    """

    return pronouncing.phones_for_word(
        word.lower()
    )
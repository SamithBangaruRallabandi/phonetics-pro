import re

from modules.pronunciation import get_arpabet
from modules.ipa import arpabet_to_ipa


def extract_words(text):
    """
    Extract English words from text.
    """

    return re.findall(
        r"[A-Za-z]+",
        text
    )


def analyze_text(text):
    """
    Analyze complete English text.
    """

    words = extract_words(text)

    results = []

    for word in words:

        arpabet = get_arpabet(word)

        if arpabet:

            ipa = arpabet_to_ipa(
                arpabet
            )

        else:

            arpabet = "Not found"
            ipa = "Not found"


        results.append({
            "Word": word,
            "ARPABET": arpabet,
            "IPA": ipa
        })


    total_words = len(results)


    recognized_words = sum(
        1
        for row in results
        if row["ARPABET"] != "Not found"
    )


    unknown_words = (
        total_words - recognized_words
    )


    recognition_rate = (
        recognized_words / total_words * 100
        if total_words > 0
        else 0
    )


    full_arpabet = " ".join(
        row["ARPABET"]
        for row in results
        if row["ARPABET"] != "Not found"
    )


    full_ipa = " ".join(
        row["IPA"]
        for row in results
        if row["IPA"] != "Not found"
    )


    return {
        "results": results,
        "total_words": total_words,
        "recognized_words": recognized_words,
        "unknown_words": unknown_words,
        "recognition_rate": recognition_rate,
        "full_arpabet": full_arpabet,
        "full_ipa": full_ipa
    }
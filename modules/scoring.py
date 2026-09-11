from modules.analyzer import analyze_text
from modules.pronunciation import get_arpabet
from modules.ipa import arpabet_to_ipa


def phonemes_from_text(text):

    analysis = analyze_text(text)

    phonemes = []

    for row in analysis["results"]:

        if row["ARPABET"] != "Not found":

            phonemes.extend(
                row["ARPABET"].split()
            )

    return phonemes


def calculate_similarity(
    expected,
    actual
):
    """
    Calculate phoneme-level similarity
    using sequence matching.
    """

    if not expected:
        return 0.0, 0

    if not actual:
        return 0.0, 0

    # Dynamic programming edit distance
    rows = len(expected) + 1
    cols = len(actual) + 1

    dp = [
        [0] * cols
        for _ in range(rows)
    ]


    for i in range(rows):
        dp[i][0] = i


    for j in range(cols):
        dp[0][j] = j


    for i in range(1, rows):

        for j in range(1, cols):

            if expected[i - 1] == actual[j - 1]:

                cost = 0

            else:

                cost = 1


            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )


    distance = dp[-1][-1]

    score = (
        max(
            0,
            1 - distance / len(expected)
        )
        * 100
    )


    matched = max(
        0,
        len(expected) - distance
    )


    return score, matched


def pronunciation_score(
    expected_text,
    recognized_text
):
    """
    Compare expected pronunciation with
    pronunciation inferred from recognized speech.
    """

    expected_analysis = analyze_text(
        expected_text
    )

    recognized_analysis = analyze_text(
        recognized_text
    )


    expected_phonemes = []

    for row in expected_analysis["results"]:

        if row["ARPABET"] != "Not found":

            expected_phonemes.extend(
                row["ARPABET"].split()
            )


    recognized_phonemes = []

    for row in recognized_analysis["results"]:

        if row["ARPABET"] != "Not found":

            recognized_phonemes.extend(
                row["ARPABET"].split()
            )


    score, matched = calculate_similarity(
        expected_phonemes,
        recognized_phonemes
    )


    return {
        "score": score,
        "matched_phonemes": matched,
        "expected_phonemes": len(
            expected_phonemes
        ),
        "expected_text": expected_text,
        "recognized_text": recognized_text,
        "expected_ipa": expected_analysis[
            "full_ipa"
        ],
        "recognized_ipa": recognized_analysis[
            "full_ipa"
        ]
    }
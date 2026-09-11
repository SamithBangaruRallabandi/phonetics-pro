# ==================================================
# ARPABET → IPA
# ==================================================

ARPABET_TO_IPA = {

    # Vowels
    "AA": "ɑ",
    "AE": "æ",
    "AH": "ʌ",
    "AO": "ɔ",
    "AW": "aʊ",
    "AY": "aɪ",
    "EH": "ɛ",
    "ER": "ɝ",
    "EY": "eɪ",
    "IH": "ɪ",
    "IY": "i",
    "OW": "oʊ",
    "OY": "ɔɪ",
    "UH": "ʊ",
    "UW": "u",

    # Consonants
    "B": "b",
    "CH": "tʃ",
    "D": "d",
    "DH": "ð",
    "F": "f",
    "G": "ɡ",
    "HH": "h",
    "JH": "dʒ",
    "K": "k",
    "L": "l",
    "M": "m",
    "N": "n",
    "NG": "ŋ",
    "P": "p",
    "R": "r",
    "S": "s",
    "SH": "ʃ",
    "T": "t",
    "TH": "θ",
    "V": "v",
    "W": "w",
    "Y": "j",
    "Z": "z",
    "ZH": "ʒ"
}


def convert_phoneme(phoneme):

    if not phoneme:
        return "", None

    stress = None

    if phoneme[-1].isdigit():

        stress = phoneme[-1]

        phoneme = phoneme[:-1]


    # Unstressed schwa
    if phoneme == "AH" and stress == "0":
        return "ə", stress


    # Unstressed r-colored schwa
    if phoneme == "ER" and stress == "0":
        return "ɚ", stress


    sound = ARPABET_TO_IPA.get(
        phoneme,
        phoneme
    )

    return sound, stress


def arpabet_to_ipa(arpabet):

    if not arpabet:
        return ""

    phonemes = arpabet.split()

    result = []

    for phoneme in phonemes:

        sound, stress = convert_phoneme(
            phoneme
        )

        if stress == "1":
            result.append("ˈ")

        elif stress == "2":
            result.append("ˌ")

        result.append(sound)

    return "".join(result)
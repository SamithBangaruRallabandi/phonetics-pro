import streamlit as st
import pandas as pd

from modules.api_client import (
    analyze_text_api,
    analyze_speech_api,
    generate_tts_api,
    score_pronunciation_api
)



# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Phonetics-PRO",
    page_icon="💬",
    layout="wide"
)


# ==================================================
# SESSION STATE
# ==================================================

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "recognized_text" not in st.session_state:
    st.session_state.recognized_text = ""

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "practice_result" not in st.session_state:
    st.session_state.practice_result = None


# ==================================================
# CALLBACKS
# ==================================================

def use_recognized_text():
    st.session_state.input_text = (
        st.session_state.recognized_text
    )


def clear_input():
    st.session_state.input_text = ""
    st.session_state.analysis = None


# ==================================================
# HEADER
# ==================================================

st.title("Phonetics-PRO")

st.write(
    "English Pronunciation Analyzer"
)

st.divider()


# ==================================================
# TEXT INPUT
# ==================================================

st.subheader("✍️ Enter Text")

text = st.text_area(
    "Type or paste English text below",
    placeholder="Example: Hello, how are you today?",
    height=150,
    key="input_text"
)


# ==================================================
# TEXT BUTTONS
# ==================================================

col1, col2 = st.columns([1, 3])

with col1:

    st.button(
        "🧹 Clear",
        use_container_width=True,
        on_click=clear_input
    )

with col2:

    generate = st.button(
        "🔊 Generate Phonetics",
        use_container_width=True
    )


# ==================================================
# GENERATE PHONETICS
# ==================================================

if generate:

    if not text.strip():

        st.warning(
            "Please enter some text."
        )

    else:

        analysis, error = analyze_text_api(
            text
        )

        if analysis:

            st.session_state.analysis = analysis

        elif error:

            st.error(error)


# ==================================================
# VOICE INPUT
# ==================================================

st.divider()

st.subheader("🎙️ Voice Input")

audio = st.audio_input(
    "Record your English speech",
    sample_rate=16000
)


if audio:

    st.audio(audio)

    speech_result, error = analyze_speech_api(
        audio
    )

    if speech_result:

        if "error" in speech_result:

            st.error(
                speech_result["error"]
            )

        else:

            speech_text = speech_result["speech_text"]

            st.success(
                "Speech recognized!"
            )

            st.write("You said:")

            st.code(
                speech_text
            )

            st.session_state.recognized_text = (
                speech_text
            )

            voice_col1, voice_col2 = st.columns(2)

            with voice_col1:

                st.button(
                    "📝 Use This Text",
                    on_click=use_recognized_text,
                    key="use_voice_text"
                )

            with voice_col2:

                analyze_voice = st.button(
                    "🎯 Analyze Speech",
                    key="analyze_voice"
                )

                if analyze_voice:

                    st.session_state.analysis = (
                        speech_result["analysis"]
                    )

                    st.success(
                        "Speech analyzed successfully!"
                    )

    elif error:

        st.error(error)


# ==================================================
# DISPLAY ANALYSIS
# ==================================================

if st.session_state.analysis:

    analysis = st.session_state.analysis

    results = analysis["results"]

    total_words = analysis["total_words"]

    recognized_words = (
        analysis["recognized_words"]
    )

    unknown_words = (
        analysis["unknown_words"]
    )

    recognition_rate = (
        analysis["recognition_rate"]
    )

    full_arpabet = (
        analysis["full_arpabet"]
    )

    full_ipa = (
        analysis["full_ipa"]
    )

    df = pd.DataFrame(results)


    # ==================================================
    # SUMMARY
    # ==================================================

    st.divider()

    st.subheader("📊 Analysis Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Words",
        total_words
    )

    col2.metric(
        "Recognized",
        recognized_words
    )

    col3.metric(
        "Unknown",
        unknown_words
    )

    col4.metric(
        "Recognition",
        f"{recognition_rate:.1f}%"
    )


    # ==================================================
    # RESULTS TABS
    # ==================================================

    tab1, tab2, tab3 = st.tabs(
        [
            "🔊 Full Pronunciation",
            "📊 Word Analysis",
            "🔉 Listen"
        ]
    )


    # ==================================================
    # FULL PRONUNCIATION
    # ==================================================

    with tab1:

        st.markdown("### IPA")

        st.code(
            full_ipa
            if full_ipa
            else "No pronunciation available"
        )

        st.markdown("### ARPABET")

        st.code(
            full_arpabet
            if full_arpabet
            else "No pronunciation available"
        )


    # ==================================================
    # WORD ANALYSIS
    # ==================================================

    with tab2:

        st.subheader(
            "Word-by-Word Analysis"
        )

        if unknown_words > 0:

            unknown_list = [
                row["Word"]
                for row in results
                if row["ARPABET"] == "Not found"
            ]

            st.warning(
                f"⚠️ {unknown_words} word(s) "
                f"could not be found: "
                + ", ".join(unknown_list)
            )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


    # ==================================================
    # TEXT TO SPEECH
    # ==================================================

    with tab3:
        st.subheader("🔊 Listen")

        if text:
            if st.button("🔊 Play Pronunciation", use_container_width=True):
                audio_data, error = generate_tts_api(text)

                if audio_data:
                    st.audio(audio_data, format="audio/mp3")
                else:
                    st.error(error)
        else:
            st.info("Enter some text first.")


# ==================================================
# PRONUNCIATION PRACTICE
# ==================================================

st.divider()

st.subheader(
    "🎯 Pronunciation Practice"
)

practice_text = st.text_input(
    "Enter a word or sentence to practice",
    placeholder="Example: pronunciation"
)


practice_audio = st.audio_input(
    "Record yourself saying the text",
    sample_rate=16000,
    key="practice_audio"
)


if practice_audio and practice_text.strip():

    st.audio(practice_audio)

    # Send audio to FastAPI for speech recognition
    speech_result, error = analyze_speech_api(
        practice_audio
    )

    if speech_result:

        if "error" in speech_result:

            st.error(speech_result["error"])

        else:

            recognized = speech_result.get("speech_text", "")

            if recognized:

                st.success(
                    f"Recognized: {recognized}"
                )

                # Send recognized text to FastAPI for scoring
                result, score_error = score_pronunciation_api(
                    practice_text,
                    recognized
                )

                if result:

                    if "error" in result:

                        st.error(result["error"])

                    else:

                        st.session_state.practice_result = result

                elif score_error:

                    st.error(score_error)

            else:

                st.error(
                    "Could not extract recognized speech."
                )

    elif error:

        st.error(error)


# ==================================================
# DISPLAY PRACTICE SCORE
# ==================================================

if st.session_state.practice_result:

    result = st.session_state.practice_result

    st.subheader(
        "🎯 Pronunciation Result"
    )

    score = result["score"]

    score_col1, score_col2 = st.columns(2)

    score_col1.metric(
        "Pronunciation Score",
        f"{score:.1f}%"
    )

    score_col2.metric(
        "Matched Phonemes",
        f"{result['matched_phonemes']} / "
        f"{result['expected_phonemes']}"
    )

    st.write(
        "**Expected text:**",
        result["expected_text"]
    )

    st.write(
        "**Recognized text:**",
        result["recognized_text"]
    )

    st.write(
        "**Expected IPA:**",
        result["expected_ipa"]
    )

    st.write(
        "**Recognized IPA:**",
        result["recognized_ipa"]
    )

    if score >= 90:

        st.success(
            "Excellent pronunciation! 🎉"
        )

    elif score >= 75:

        st.info(
            "Good pronunciation. Keep practicing! 👍"
        )

    elif score >= 50:

        st.warning(
            "Fair pronunciation. More practice is needed."
        )

    else:

        st.error(
            "Try again and focus on the individual sounds."
        )
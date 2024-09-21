import streamlit as st
from gtts import gTTS
import io
from langdetect import detect, LangDetectException
from gtts.lang import tts_langs

# Function to detect the language of the input text
def detect_language(input_text):
    try:
        detected_lang = detect(input_text)
        return detected_lang
    except LangDetectException:
        return 'en'  # Default to English if language cannot be detected

# Function to convert text to speech using gTTS
def generate_audio_gtts(input_text, selected_voice):
    # Detect the language of the input text
    detected_lang = detect_language(input_text)

    # Fetch available languages in gTTS
    available_langs = tts_langs()

    # If the detected language is not available, default to English
    if detected_lang not in available_langs:
        detected_lang = 'en'

    # Voice descriptions for clarity and accessibility
    slow_speech = True  # Set speech to slow for accessibility for elderly listeners
    if selected_voice == "Female Voice":
        tts = gTTS(text=input_text, lang=detected_lang, slow=slow_speech)
    else:
        tts = gTTS(text=input_text, lang=detected_lang, slow=slow_speech)

    # Save the generated audio to a buffer
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)  # Reset buffer pointer for playback

    return audio_buffer, detected_lang

def main():
    # Streamlit app layout with accessibility in mind
    st.title("📖 Text to Speech Converter for the Elderly")
    st.write("*Convert your written text into speech using AI.*")

    # Input text box
    input_text = st.text_area("Text to convert:", height=200, max_chars=1000, placeholder="Paste or type your article here...")

    # Voice selection
    voice_options = ["Female Voice", "Male Voice"]
    selected_voice = st.selectbox("Choose voice:", voice_options)

    # Convert button
    if st.button("Convert to Speech"):
        if input_text:
            try:
                # Generate audio using gTTS
                audio_buffer, detected_lang = generate_audio_gtts(input_text, selected_voice)
                # Display detected language
                st.info(f"Detected Language: {detected_lang.upper()}")

                # Play audio directly from memory
                st.audio(audio_buffer, format='audio/wav')

            except Exception as e:
                st.error(f"Error generating audio: {e}")
        else:
            st.warning("Please enter some text.")

    # Instructions for use
    st.markdown("### Instructions:")
    st.markdown("1. Paste or type your article text in the box above.")
    st.markdown("2. Choose your preferred voice.")
    st.markdown("3. Click 'Convert to Speech' to listen to the audio.")

    # Add team credit at the bottom of the page
    st.markdown("<br><br><center><b>MADE BY TEAM IRJJ 😝</b></center>", unsafe_allow_html=True)

# Entry point for the Streamlit app
if __name__ == "__main__":
    main()

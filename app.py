import streamlit as st
from gtts import gTTS
from google_trans_new import google_translator
import io
from gtts.lang import tts_langs

# Initialize translator
translator = google_translator()

# Function to translate text to selected language
def translate_text(input_text, target_language):
    translated = translator.translate(input_text, lang_tgt=target_language)
    return translated

# Function to convert text to speech using gTTS
def generate_audio_gtts(translated_text, selected_language, selected_voice):
    try:
        # Voice descriptions for clarity and accessibility
        slow_speech = True  # Set speech to slow for accessibility for elderly listeners
        tts = gTTS(text=translated_text, lang=selected_language, slow=slow_speech)

        # Save the generated audio to a buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)  # Reset buffer pointer for playback

        return audio_buffer

    except Exception as e:
        raise Exception(f"Error generating audio: {e}")

def main():
    # Streamlit app layout with accessibility in mind
    st.title("📖 Text to Speech Converter for the Elderly")
    st.write("*Convert your written text into speech using AI.*")

    # Input text box
    input_text = st.text_area("Text to convert:", height=200, max_chars=1000, placeholder="Paste or type your article here...")

    # Voice selection
    voice_options = ["Female Voice", "Male Voice"]
    selected_voice = st.selectbox("Choose voice:", voice_options)

    # Language selection
    available_languages = tts_langs()  # Fetch available languages
    selected_language = st.selectbox("Choose language for translation and speech:", list(available_languages.items()), format_func=lambda x: f"{x[1]} ({x[0]

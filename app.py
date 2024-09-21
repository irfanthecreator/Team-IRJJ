import streamlit as st
from gtts import gTTS
from googletrans import Translator
import io
from gtts.lang import tts_langs

# Initialize translator
translator = Translator()

# Function to translate text to selected language
def translate_text(input_text, target_language):
    translated = translator.translate(input_text, dest=target_language)
    return translated.text

# Function to convert text to speech using gTTS
def generate_audio_gtts(translated_text, selected_language, selected_voice):
    # Voice descriptions for clarity and accessibility
    slow_speech = True  # Set speech to slow for accessibility for elderly listeners
    tts = gTTS(text=translated_text, lang=selected_language, slow=slow_speech)

    # Save the generated audio to a buffer
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)  # Reset buffer pointer for playback

    return audio_buffer

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
    selected_language = st.selectbox("Choose language for translation and speech:", list(available_languages.items()), format_func=lambda x: f"{x[1]} ({x[0]})")

    # Convert button
    if st.button("Convert to Speech"):
        if input_text:
            try:
                # Translate the text to the selected language
                translated_text = translate_text(input_text, selected_language[0])

                # Generate audio using gTTS with the translated text
                audio_buffer = generate_audio_gtts(translated_text, selected_language[0], selected_voice)

                # Display the translated text
                st.write(f"Translated text ({selected_language[1]}): {translated_text}")

                # Play audio directly from memory
                st.audio(audio_buffer, format='audio/wav')

            except Exception as e:
                st.error(f"Error generating audio: {e}")
        else:
            st.warning("Please enter some text.")

    # Instructions for use
    st.markdown("### Instructions:")
    st.markdown("1. Paste or type your article text in the box above.")
    st.markdown("2. Choose your preferred voice and language.")
    st.markdown("3. Click 'Convert to Speech' to listen to the audio.")

    # Add team credit at the bottom of the page
    st.markdown("<br><br><center><b>MADE BY TEAM IRJJ 😝</b></center>", unsafe_allow_html=True)

# Entry point for the Streamlit app
if __name__ == "__main__":
    main()

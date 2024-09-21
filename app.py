import streamlit as st
from gtts import gTTS
import io
from deep_translator import GoogleTranslator

# Function to convert text to speech using gTTS
def generate_audio_gtts(translated_text, selected_language):
    tts = gTTS(text=translated_text, lang=selected_language, slow=True)
    
    # Save the generated audio to a buffer
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)  # Reset buffer pointer for playback

    return audio_buffer

# Function to translate text using deep-translator
def translate_text(input_text, target_language):
    translated_text = GoogleTranslator(source='auto', target=target_language).translate(input_text)
    return translated_text

def main():
    # Streamlit app layout with accessibility in mind
    st.title("📖 Text to Speech Converter for the Elderly with Language Translation")
    st.write("*Convert your written text into speech in multiple languages.*")

    # Input text box
    input_text = st.text_area("Text to convert:", height=200, max_chars=1000, placeholder="Paste or type your article here...")

    # Language selection for translation with correct language codes
    language_options = {
        'English': 'en',
        'French': 'fr',
        'Spanish': 'es',
        'German': 'de',
        'Korean': 'ko',
        'Chinese (Simplified)': 'zh-CN',
        'Chinese (Traditional)': 'zh-TW',
        'Japanese': 'ja',
        'Italian': 'it',
        'Hindi': 'hi'
    }
    selected_language = st.selectbox("Choose target language for translation:", list(language_options.keys()))

    # For gTTS, voice selection is not supported in non-English languages.
    # Simplify this part and only allow male/female selection for English.
    if selected_language == 'English':
        voice_options = ["Female Voice", "Male Voice"]
        selected_voice = st.selectbox("Choose voice:", voice_options)
    else:
        st.write("Voice selection is not supported for this language, using default voice.")
        selected_voice = "Default"

    # Convert button
    if st.button("Convert to Speech"):
        if input_text:
            try:
                # Translate the text to the selected language
                target_language_code = language_options[selected_language]
                translated_text = translate_text(input_text, target_language_code)

                # Generate audio using gTTS
                audio_buffer = generate_audio_gtts(translated_text, target_language_code)

                # Play audio directly from memory
                st.audio(audio_buffer, format='audio/wav')
                st.write(f"**Translated Text ({selected_language}):** {translated_text}")

            except Exception as e:
                st.error(f"Error generating audio: {e}")
        else:
            st.warning("Please enter some text.")

    # Instructions for use
    st.markdown("### Instructions:")
    st.markdown("1. Paste or type your article text in the box above.")
    st.markdown("2. Choose your preferred voice and target language.")
    st.markdown("3. Click 'Convert to Speech' to translate and listen to the audio.")

    # Add team credit at the bottom of the page
    st.markdown("<br><br><center><b>MADE BY TEAM IRJJ 😝</b></center>", unsafe_allow_html=True)

# Entry point for the Streamlit app
if __name__ == "__main__":
    main()

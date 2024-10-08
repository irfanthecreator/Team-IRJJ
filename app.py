import streamlit as st
from gtts import gTTS
import io
from deep_translator import GoogleTranslator
import pdfplumber  # Alternative PDF text extraction
from PIL import Image  # To open image files
import requests
from bs4 import BeautifulSoup

# Function to convert text to speech using gTTS
def generate_audio_gtts(translated_text, selected_language, speech_speed):
    tts = gTTS(text=translated_text, lang=selected_language, slow=speech_speed)
    
    # Save the generated audio to a buffer
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)  # Reset buffer pointer for playback

    return audio_buffer

# Function to translate text using deep-translator
def translate_text(input_text, target_language):
    translated_text = GoogleTranslator(source='auto', target=target_language).translate(input_text)
    return translated_text

# Function to extract text from a PDF file using pdfplumber
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()  # Extract text from each page
    return text

# Placeholder for image processing (without OCR for now)
def extract_text_from_image(image_file):
    return "Image text extraction feature is not available in this environment."

# Function to fetch and validate text length from URL
def fetch_text_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            if len(text) > 5000:
                st.error("The content fetched from the URL exceeds 5000 characters. Please provide a shorter article.")
                return None
            return text
        else:
            st.error("Failed to fetch content from the URL. Please check the link and try again.")
            return None
    except Exception as e:
        st.error(f"Error fetching text from URL: {e}")
        return None

def main():
    # Streamlit app layout with accessibility in mind
    st.title("**Fun & Accessible Text to Speech Converter**")
    
    # Explanation of the app's purpose for elderly users with vision problems
    st.markdown("""
    ### 🧓👴 **Purpose of the App:**
    This app is designed to help elderly users with declining eyesight by converting text into speech 🔊. 
    Instead of reading, users can now listen 👂 to articles, news, or important documents, in different languages! 🌍
    Let's make information accessible for everyone! 
    """)
    
    st.write("*Convert your written text into speech in multiple languages, or extract text from PDFs for conversion.*")

    # Input method selection
    input_option = st.radio("**Choose how you want to input your text:**", ("✍️ Type/Paste Text", "📄 Upload PDF", "📸 Upload Image", "🌐 Enter URL"))

    input_text = ""

    if input_option == "✍️ Type/Paste Text":
        # Input text box with larger placeholder text for readability
        input_text = st.text_area("📝 **Type or Paste your text here**", height=200, max_chars=1000, placeholder="Paste or type your text here...", help="Enter the text you want to convert into speech.")
    
    elif input_option == "📄 Upload PDF":
        # File uploader for PDF
        pdf_file = st.file_uploader("📄 **Upload a PDF file**", type=["pdf"])
        if pdf_file is not None:
            input_text = extract_text_from_pdf(pdf_file)
            st.write("**Extracted text from PDF:**")
            st.write(input_text)
    
    elif input_option == "📸 Upload Image":
        # Caution: Image to Text extraction won't work in the Streamlit Cloud environment
        st.warning("⚠️ **Note:** Image text extraction (OCR) is not supported in the current Streamlit environment.")
        image_file = st.file_uploader("📸 **Upload an image file**", type=["png", "jpg", "jpeg"])
        if image_file is not None:
            input_text = extract_text_from_image(image_file)
            st.write("**Extracted text from image:**")
            st.write(input_text)

    elif input_option == "🌐 Enter URL":
        # URL input field
        url = st.text_input("🌐 **Enter the URL of the article or document**")
        if url:
            input_text = fetch_text_from_url(url)
            if input_text:
                st.write("**Extracted text from URL:**")
                st.write(input_text)
            st.markdown("⚠️ **Note:** If you're inputting text from a URL, ensure the content does not exceed 5000 characters. Long texts or articles may cause errors.")

    # Language selection for translation with correct language codes
    language_options = {
        '🇬🇧 English': 'en',
        '🇫🇷 French': 'fr',
        '🇪🇸 Spanish': 'es',
        '🇩🇪 German': 'de',
        '🇰🇷 Korean': 'ko',
        '🇨🇳 Chinese (Simplified)': 'zh-CN',
        '🇹🇼 Chinese (Traditional)': 'zh-TW',
        '🇯🇵 Japanese': 'ja',
        '🇮🇹 Italian': 'it',
        '🇮🇳 Hindi': 'hi'
    }
    selected_language = st.selectbox("🌍 **Choose your target language**:", list(language_options.keys()), help="Select the language you want to hear the audio in.")

    # Speech speed slider
    speech_speed = st.slider("⏩ **Select Speech Speed**:", min_value=0.5, max_value=1.5, value=1.0, step=0.1, help="Adjust the speed of the speech (slower or faster).")

    # Convert button
    if st.button("🔊 **Convert to Speech**"):
        if input_text:
            try:
                # Translate the text to the selected language
                target_language_code = language_options[selected_language]
                translated_text = translate_text(input_text, target_language_code)

                # Generate audio using gTTS
                audio_buffer = generate_audio_gtts(translated_text, target_language_code, speech_speed < 1.0)

                # Play audio directly from memory
                st.audio(audio_buffer, format='audio/wav')
                st.write(f"🗣️ **Translated Text ({selected_language}):** {translated_text}")

            except Exception as e:
                st.error(f"🚨 Error generating audio: {e}")
        else:
            st.warning("⚠️ **Please enter or upload some text.**")

    # Funky Instructions with emojis and clearer explanation
    st.markdown("### 📜 **Instructions:**")
    st.markdown("1. ✍️ **Choose how to input your text:** Type, upload a PDF, upload an image (OCR not supported), or enter a URL.")
    st.markdown("2. 🌍 **Select your target language** for translation.")
    st.markdown("3. 🔊 **Click 'Convert to Speech'** to translate the text and listen to the audio!")

    # Fun footer with team credit
    st.markdown("<br><br><center><b style='font-size: 22px;'>MADE BY TEAM IRJJ :flag-kr: :flag-sg:</b></center>", unsafe_allow_html=True)

# Entry point for the Streamlit app
if __name__ == "__main__":
    main()

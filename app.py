import streamlit as st
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import numpy as np
import io
import librosa

# Cache the model to avoid reloading it on every run
@st.cache_resource
def load_model_and_tokenizer():
    device = "cpu"
    repo_id = "parler-tts/parler_tts_mini_v0.1"  # Use the correct model
    model = ParlerTTSForConditionalGeneration.from_pretrained(repo_id).to(device)
    tokenizer = AutoTokenizer.from_pretrained(repo_id)
    return model, tokenizer

def generate_audio(input_text, selected_voice, speed):
    # Simplified voice descriptions
    description = "female voice" if selected_voice == "Female Voice" else "male voice"

    # Tokenize the input text and description
    input_ids = tokenizer(description, return_tensors="pt").input_ids.to("cpu")
    prompt_input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to("cpu")

    # Generate the speech audio using the model
    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()

    # Normalize audio to prevent clipping
    max_abs_value = np.max(np.abs(audio_arr))
    if max_abs_value > 0:
        audio_arr = audio_arr / max_abs_value

    # Adjust speed using time-stretching without changing pitch
    if speed != 1.0:
        audio_arr = librosa.effects.time_stretch(audio_arr, rate=speed)

    # Convert the numpy array into bytes buffer instead of saving to a file
    audio_buffer = io.BytesIO()
    sf.write(audio_buffer, audio_arr, samplerate=model.config.sampling_rate, format="WAV")
    audio_buffer.seek(0)  # Reset buffer pointer

    return audio_buffer

def main():
    # Load model and tokenizer with feedback spinner
    with st.spinner('Loading Text-to-Speech Model...'):
        global model, tokenizer
        model, tokenizer = load_model_and_tokenizer()

    # Streamlit app layout with accessibility in mind
    st.title("📖 Text to Speech Converter for the Elderly")
    st.write("*Convert your written text into speech using AI.*")

    # Input text box
    input_text = st.text_area("Text to convert:", height=200, max_chars=1000, placeholder="Paste or type your article here...")

    # Voice selection
    voice_options = ["Female Voice", "Male Voice"]
    selected_voice = st.selectbox("Choose voice:", voice_options)

    # Speed control
    speed = st.slider("Select speed:", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

    # Convert button
    if st.button("Convert to Speech"):
        if input_text:
            try:
                # Generate audio
                audio_buffer = generate_audio(input_text, selected_voice, speed)
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
    st.markdown("3. Adjust the speed if needed.")
    st.markdown("4. Click 'Convert to Speech' to listen to the audio.")

    # Add team credit at the bottom of the page
    st.markdown("<br><br><center><b>MADE BY TEAM IRJJ 😝</b></center>", unsafe_allow_html=True)

# Entry point for the Streamlit app
if __name__ == "__main__":
    main()

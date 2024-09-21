import streamlit as st
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import numpy as np
import io

# Cache the model to avoid reloading it on every run
@st.cache_resource
def load_model_and_tokenizer():
    device = "cpu"
    repo_id = "parler-tts/parler_tts_mini_v0.1"
    model = ParlerTTSForConditionalGeneration.from_pretrained(repo_id).to(device)
    tokenizer = AutoTokenizer.from_pretrained(repo_id)
    return model, tokenizer

# Preprocess text to improve smoothness
def preprocess_text(input_text):
    # Split the text into sentences to make the model handle sentence boundaries better
    sentences = input_text.strip().split(". ")
    processed_text = [sentence + "." for sentence in sentences if sentence]
    return processed_text

def generate_audio(input_text, selected_voice):
    # Improved voice descriptions for clarity, slower speed, and easier listening for the elderly
    if selected_voice == "Female Voice":
        description = "A clear, slow, and soft-spoken female voice with distinct articulation, perfect for elderly listeners."
    else:
        description = "A slow, calm, and soothing male voice, speaking clearly and at a measured pace, ideal for elderly listeners."

    # Preprocess text for smoother output
    processed_text = preprocess_text(input_text)

    # Initialize audio buffer to concatenate multiple sentence outputs
    full_audio = []

    for sentence in processed_text:
        input_ids = tokenizer(description, return_tensors="pt").input_ids.to("cpu")
        prompt_input_ids = tokenizer(sentence, return_tensors="pt").input_ids.to("cpu")

        # Generate the speech audio using greedy decoding (no beam search)
        generation = model.generate(
            input_ids=input_ids,
            prompt_input_ids=prompt_input_ids,
            num_beams=1,                   # Set to 1 for greedy decoding
            num_beam_groups=1,             # Also set this to 1 for compatibility
            max_length=500,                # Increase max_length to ensure complete sentences
            no_repeat_ngram_size=3,         # Avoid repetition
            early_stopping=True             # Stop early if necessary
        )
        audio_arr = generation.cpu().numpy().squeeze()

        # Normalize audio to prevent clipping
        max_abs_value = np.max(np.abs(audio_arr))
        if max_abs_value > 0:
            audio_arr = audio_arr / max_abs_value

        # Append each sentence's audio output to the full audio list
        full_audio.append(audio_arr)

    # Concatenate all the audio segments into a single array
    full_audio_arr = np.concatenate(full_audio)

    # Convert the numpy array into bytes buffer instead of saving to a file
    audio_buffer = io.BytesIO()
    sf.write(audio_buffer, full_audio_arr, samplerate=model.config.sampling_rate, format="WAV")
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

    # Convert button
    if st.button("Convert to Speech"):
        if input_text:
            try:
                # Generate audio
                audio_buffer = generate_audio(input_text, selected_voice)
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

import streamlit as st
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
import soundfile as sf
import numpy as np
import io
import librosa

# Cache the model to avoid reloading it on every run
@st.cache_resource
def load_model_and_processor():
    device = "cpu"
    model_id = "facebook/mms-tts-eng"
    model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id).to(device)
    processor = AutoProcessor.from_pretrained(model_id)
    return model, processor

def generate_audio(input_text, speed):
    model, processor = load_model_and_processor()

    # Prepare input text
    inputs = processor(input_text, return_tensors="pt").to("cpu")

    # Generate the speech audio using the model
    with torch.no_grad():
        speech = model.generate(**inputs)
    
    # Convert to numpy array
    audio_arr = speech.cpu().numpy().squeeze()

    # Normalize audio to prevent clipping
    max_abs_value = np.max(np.abs(audio_arr))
    if max_abs_value > 0:
        audio_arr = audio_arr / max_abs_value

    # Adjust speed using time-stretching without changing pitch
    if speed != 1.0:
        audio_arr = librosa.effects.time_stretch(audio_arr, rate=speed)

    # Convert the numpy array into bytes buffer instead of saving to a file
    audio_buffer = io.BytesIO()
    sf.write(audio_buffer, audio_arr, samplerate=16000, format="WAV")  # Assuming 16kHz sample rate
    audio_buffer.seek(0)  # Reset buffer pointer

    return audio_buffer

def main():
    st.title("📖 Text to Speech Converter")

    input_text = st.text_area("Text to convert:", height=200, max_chars=1000, placeholder="Paste or type your article here...")

    speed = st.slider("Select speed:", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

    if st.button("Convert to Speech"):
        if input_text:
            try:
                audio_buffer = generate_audio(input_text, speed)
                st.audio(audio_buffer, format='audio/wav')

            except Exception as e:
                st.error(f"Error generating audio: {e}")
        else:
            st.warning("Please enter some text.")

    st.markdown("<br><br><center><b>MADE BY TEAM IRJJ 😝</b></center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

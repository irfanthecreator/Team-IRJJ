# Text-to-Speech Converter for the Elderly

**Team IRJJ 😝**

Team website: https://sites.google.com/yanggok.hs.kr/teamirjj/home-%ED%99%88

Link: https://team-irjj.streamlit.app/

## Overview
This project is a text-to-speech (TTS) converter designed to improve accessibility for elderly individuals with declining eyesight. The application allows users to input text (such as articles, news, and documents) and convert it into clear, spoken speech, which can be played back to them. The goal is to assist the elderly in keeping up with essential information, helping them maintain their quality of life.

Initially, we trained the project using the **Parler-TTS** model for text-to-speech conversion, and later we optimized the model for deployment on **Streamlit**.

## Problem Scoping using 4Ws:

### Who (누구):
The users who are facing this problem are elderly people who have difficulty reading due to declining eyesight.  
이 문제에 직면한 사용자는 시력 저하로 인해 읽기가 어려운 노인입니다.

### What (무엇):
They find it difficult to read articles, news, and important information and documents.  
기사, 뉴스, 중요한 정보 및 문서를 읽기 어렵습니다.

### Where (어디):
This solution can be used in various places such as homes, libraries, and community centers. It is available as both a mobile app and a web application.  
가정, 도서관, 커뮤니티 센터 등 다양한 장소에서 사용할 수 있으며 모바일 앱 또는 웹 애플리케이션 형태로 제공될 예정입니다.

### Why (왜):
The solution aims to enhance accessibility for the elderly, improving their understanding of important information. Reading is vital for cognitive stimulation and emotional well-being, helping users maintain social engagement and improve their quality of life.  
이 솔루션은 노인들의 접근성을 향상시켜 중요한 정보에 대한 이해를 높이는 것을 목표로 합니다. 독서는 인지 자극과 정서적 웰빙에 필수적이며 사용자가 사회적 참여를 유지하고 삶의 질을 향상시키는 데 도움이 됩니다.

## Parler-TTS and OpenVINO™ Integration

### What is Parler-TTS?
**Parler-TTS** is a lightweight text-to-speech model that generates high-quality, natural-sounding speech. It allows control over speaker identity, style, and conditions, using natural language descriptions, making it ideal for creative applications.

The model was trained on a 45k-hour dataset and uses scalable methods to label various aspects of speaker identity, style, and recording conditions. This method enables the creation of a speech language model that significantly improves audio fidelity.

For more details, see the original paper [Natural language guidance of high-fidelity text-to-speech with synthetic annotations](https://www.text-description-to-speech.com/) by Dan Lyth and Simon King from Stability AI and Edinburgh University.

![Architecture](https://images.squarespace-cdn.com/content/v1/657816dfbefe0533e8a69d9a/30c96e25-acc5-4019-acdd-648da6142c4c/architecture_v3.png?format=2500w)

### How Parler-TTS was used:
Initially, we implemented **Parler-TTS** to generate the speech output in this application. Using OpenVINO™, we converted the model for more optimized, real-time inference and improved processing speeds.

We chose Parler-TTS because of its flexibility and ability to control the generated speech characteristics using natural language descriptions, which allowed us to provide clear, slow, and easy-to-understand speech suitable for elderly listeners.

### Steps taken:
1. **Loading the Parler-TTS Model**: We used the pretrained **Parler-TTS** model to convert input text to speech, which we initially deployed using **Streamlit** for web and mobile applications.
2. **OpenVINO™ Optimization**: After loading the model, we converted it to OpenVINO™ IR format for faster inference times.
3. **Model Compilation and Inference**: After converting the model, we compiled it with OpenVINO™ and ran inference for interactive user inputs.
4. **Final Streamlit Integration**: The application was further optimized and deployed on **Streamlit** to make it accessible via web interfaces.

For more information on Parler-TTS and OpenVINO, visit:  
- [GitHub repository](https://github.com/huggingface/parler-tts)  
- [HuggingFace page](https://huggingface.co/parler-tts)

## Features
- Converts written text into spoken speech.
- Two voice options: Clear, slow, and soft-spoken female voice, and calm, soothing male voice.
- Designed specifically with elderly users in mind, providing slower and clearer speech output.
- Fully available as a web application using Streamlit for easy deployment and usage.

## Installation
To set up this project on your local machine or for deployment, follow these steps:

1. Clone this repository:
   ```bash
   git clone https://github.com/irfanthecreator/Team-IRJJ.git

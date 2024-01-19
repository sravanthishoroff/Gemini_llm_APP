from dotenv import load_dotenv
load_dotenv()  

import streamlit as st
import os
from PIL import Image

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses for text
def get_gemini_text_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

# Function to load Gemini Pro model and get responses for chatbot
def get_gemini_chat_response(question, chat):
    response = chat.send_message(question, stream=True)
    return response

# Function to load Gemini Pro Vision model and get responses for images
def get_gemini_vision_response(input_text, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, image])
    return response.text

# Initialize streamlit app
st.set_page_config(page_title="Gemini Multi-Mode App")

st.header("Gemini Multi-Mode Application")

# Dropdown to select mode
selected_mode = st.selectbox("Select Mode", ["Text", "Chatbot", "Vision"])

if selected_mode == "Text":
    st.subheader("Text Mode")
    input_text = st.text_input("Input Prompt:", key="input_text")
    submit_text = st.button("Generate Text")

    if submit_text and input_text:
        response_text = get_gemini_text_response(input_text)
        st.subheader("The Response is")
        st.write(response_text)

elif selected_mode == "Chatbot":
    st.subheader("Chatbot Mode")
    input_chat = st.text_input("Input Question:", key="input_chat")
    submit_chat = st.button("Ask the Chatbot")

    # Initialize chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    if submit_chat and input_chat:
        # Load or create chat history
        if 'chat' not in st.session_state:
            st.session_state['chat'] = genai.GenerativeModel("gemini-pro").start_chat(history=[])

        response_chat = get_gemini_chat_response(input_chat, st.session_state['chat'])
        st.subheader("The Response is")
        for chunk in response_chat:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("You", input_chat))
            st.session_state['chat_history'].append(("Bot", chunk.text))

        st.subheader("The Chat History is")
        for role, text in st.session_state['chat_history']:
            st.write(f"{role}: {text}")

elif selected_mode == "Vision":
    st.subheader("Vision Mode")
    input_vision_text = st.text_input("Input Prompt:", key="input_vision_text")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

    submit_vision = st.button("Tell me about the image")

    if submit_vision and uploaded_file:
        response_vision = get_gemini_vision_response(input_vision_text, image)
        st.subheader("The Response is")
        st.write(response_vision)

from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# function 
def get_gemini_response(question):
    response = chat.send_message(question,stream=True)
    return response

# initiate streamlit APP
st.set_page_config(page_title="ChatBot")

st.header("Gemini Pro App")

input = st.text_input("Input: ", key="input")
submit = st.button("Ask your question")

if submit:
    response = get_gemini_response(input)
    st.subheader("The Response is: ")
    for chunk in response:
        print(chunk.text)
        print("_"*80)

    st.write(chat.history)

from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function for calling Gemini_pro model
model = genai.GenerativeModel("gemini-pro")
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

# streamlit app
st.set_page_config(page_title="Demo")

st.header("Gemini Pro App")

input = st.text_input("Input: ", key="input")
submit = st.button("Ask your question")

if submit:
    response = get_gemini_response(input)
    st.subheader("The response is:")
    st.write(response)
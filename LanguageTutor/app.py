import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def get_gemini_response(query,prompt):
    response = model.generate_content([query,prompt])
    return response.text

st.set_page_config(page_title="Language Tutor")
st.header("AI Language Tutor")

input = st.text_input("Provide the language you want to learn",key=input)

input_prompt = f"""
You are an expert Linguistic Tutor who is proficient in teaching {input} language. Your task is to provide a roadmap to learn the language efficiently. Additionally it should provide resources to be used, duration to complete each task.
"""
submit = st.button("Language Tutor")

if submit:
    st.subheader("The Response is being generated")
    response = get_gemini_response(input,input_prompt)
    st.write(response)
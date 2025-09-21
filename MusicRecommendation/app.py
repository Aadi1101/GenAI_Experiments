from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(query,prompt):
    response = model.generate_content([query,prompt])
    return response.text

st.set_page_config(page_title="Music Recommendation System")
st.header("Music Recommendation System")
input_text = st.text_input("Input...",key="input")
submit = st.button("Recommend Songs")

input_prompt = """
You are an expert Music Jokey who is aware of each and every music and song composition in the world. Your task is to suggest songs based on the description provided. If the recommended songs turns the mood to sad immediately start recommending songs with energetic and joyful mood. The response should be in below format:

1. Song Name 1 :- Artist 1 Name
2. Song Name 2 :- Artist 2 Name
3. Song Name 3 :- Artist 3 Name
"""

if submit:
    response = get_gemini_response(input_prompt,input_text)
    st.subheader("The Response is:")
    st.write(response)
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

st.set_page_config(page_title="Data Structures and Algorithms Bot")
st.header("Data Structures and Algorithms Bot")
input = st.text_input("Input:",key="input")
submit = st.button("Tell me about...")

input_prompt = """
You are an expert in solving Data Structures and Algorithms. Your knowledge about Data Structures and Algorithms is exceptional. Your task is to answer the query passed by the user in detail with it's implementation containing the general approach as well the optimized approach. Additionally provide the questions needed to solve for getting used to that concept in addition to this answer those questions as well. Also provide online resources to practice specified topic. Also provided which are the related topics to the specified one.
"""

if submit:
    st.subheader("The Response is...")
    response = get_gemini_response(input,input_prompt)
    st.write(response)
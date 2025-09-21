import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text

st.set_page_config(page_title="Use Case Builder")
st.header("Gemini Generative AI Use Case Builder")
submit = st.button("Suggest me an Use Case.")

input_prompt = """
You are an expert in suggesting an use case for building a mini project in Generative AI using gemini-1.5-flash model an organization. Your task is to provide summary of the project with a detailed workflow to implement the project. Furthermore you should keep in mind the use case which you are suggesting must be unique and it's primary technology requirement should be Python Programming Language.
"""

if submit:
    response = get_gemini_response(input_prompt)
    st.subheader("The Response is")
    st.write(response)
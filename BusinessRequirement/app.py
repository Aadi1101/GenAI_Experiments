from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
import markdown
import pdfkit

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(question,prompt):
    response = model.generate_content([question,prompt])
    return response.text

def to_pdf(text):
    html_content = markdown.markdown(text)
    pdfkit.from_string(html_content,'output.pdf')
    return "Done"
st.set_page_config("Business Requirement Analysis")
st.header("Gemini LLM App")
input = st.text_input("Input: ",key="input")
submit1 = st.button("Ask the Question")

input_prompt = """
You are an expert Business Analyst in every field, your task is to provide the technical, non technical requirements based on the project description, Additionally you have to provide the team required with skills and designation to complete the project and estimated cost of the project in Indian Rupees. Firstly provide Summary of the project followed by Technical and Non Technical requirements then the team details and finally the estimated cost of the project in Indian Rupees.
"""

if submit1:
    response = get_gemini_response(input_prompt,input)
    st.subheader("The Response is being generated...")
    print(to_pdf(response))
    st.write(response)
    
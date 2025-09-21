from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question,stream=True)
    return response

st.set_page_config(page_title="Conversational Bot")
st.header("Gemini Conversational Bot")

if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: ",key="input")
submit = st.button("Ask Question")

if submit and input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(("You",input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot",chunk.text))
st.subheader("The Chat History is")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
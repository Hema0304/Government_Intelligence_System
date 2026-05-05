import streamlit as st
from groq import Groq 
#Groq model
import streamlit as st
from langchain_groq import ChatGroq

client = Groq(
    model="llama-3.1-8b-instant",
    api_key=st.secrets["GROQ_API_KEY"]
)
def generate_response(prompt):
    response = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content




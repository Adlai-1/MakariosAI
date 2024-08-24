import os, sys
import streamlit as st
sys.path.append(os.path.abspath(os.path.dirname("rag_model")))
from rag_model.model import call_rag

st.title("MakariosAI")
st.text("""
Your AI that provides an interactive enviroment for every book written by  
Bishop Dag Heward-Mills.
""")

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# open file book
books = []
try:
    with open("books.txt") as file:
        for line in file:
            books.append(line.strip())
        books.sort()
except Exception as e:
    print(f"Error: {e}") 

# side bar
with st.sidebar:
    st.header(f"Library", divider="gray")
    for book in books:
        st.text(book)
    st.caption("The list above indicate the books available for MakariosAI.")

# conversations...
if text := st.chat_input("Message MakariosAI"):
    st.chat_message("user").markdown(text)
    st.session_state.messages.append({"role": "user", "content": text})

    try:
        resp = call_rag(text, st.session_state.messages)
        with st.chat_message("ai"):
            st.markdown(resp)
            st.session_state.messages.append({"role": "ai", "content": resp})
    
    except Exception as error:
        with st.chat_message("ai"):
            text = "Unable to give a response, try again later!"
            st.markdown(resp)
            st.session_state.messages.append({"role": "ai", "content": text})
        print(error)
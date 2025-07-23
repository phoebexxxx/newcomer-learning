import streamlit as st

st.set_page_config(page_title="Welcome", layout="centered")

st.title("👋 Welcome to the Wikipedia Editing Study")
st.markdown("""
Thank you for participating in our study!

This short activity will guide you through a Wikipedia editing task, 
assisted by an AI model. You will:

- Enter your participant information
- Be assigned to a group
- Interact with the AI assistant
- Complete an article editing task

Click the page on the left sidebar to get started.
""")

st.info("Please go to **'1. Participant Info'** in the sidebar to begin.")

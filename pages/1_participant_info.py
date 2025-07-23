import streamlit as st

st.set_page_config(page_title="Participant Info", layout="centered")
st.title("👤 Participant Information")

# Initialize session state
if "participant_id" not in st.session_state:
    st.session_state.participant_id = ""
if "group" not in st.session_state:
    st.session_state.group = ""

# Input fields
st.session_state.participant_id = st.text_input("Enter your Participant ID:", st.session_state.participant_id)
st.session_state.group = st.selectbox("Select your Group:", ["", "Group A", "Group B"])

# Navigation
if st.session_state.participant_id and st.session_state.group:
    st.success("✅ You're ready to begin.")
    st.markdown("Please click the button to start the task.")
    if st.button("✅ I am ready!"):
        st.switch_page("pages/2_main_study.py")  
else:
    st.warning("Please complete both fields to continue.")

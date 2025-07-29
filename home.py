import streamlit as st

st.set_page_config(page_title="Welcome", layout="centered")

st.title("👋 Welcome to Wiki-newcomer Study")
st.markdown("""
Thank you for participating in our study! We truly appreciate your time and contribution to the study!

This 60-90 minute study includes the following steps: 

1. Enter your participant ID and group information
2. Complete a Wikipedia article editing task
3. Complete a follow up task
4. Fill out surveys 
5. Participate in an short interview (if selected)
            
Before you start, it is important to note: 
            
- Please **DO NOT** use the sidebar on the left unless you are instructed to do so. The sidebar is to show your progress through the study.
            Clicking on it will cause **data loss**, and require you to start over. 
- Please read the instruction on each page carefully before making any changes. 
- We ask you to share your entire screen (rather than a specific window), so we can record the session for data analysis purposes. You are weclome to turn off your camera, but we do need audio. 
- Please note that this study does **not** offer monetary compensation, and we thank you for your contribution to understanding human AI interaction.
- The researcher will be present throughout the session, feel free to ask any questions at any time.
""")

st.info("When you are ready, please click the button below to continue.")
if st.button("Next"):
        st.session_state.welcome_done = True
        st.switch_page("pages/1_participant_info.py")  

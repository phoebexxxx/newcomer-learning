import streamlit as st

if not st.session_state.get("followup_done"): 
    st.warning("Please finish Follow Up first.")
    st.stop()

st.set_page_config(page_title="Post Task Surveys", layout="wide")
st.title("🧠 Post-Task Surveys")

st.markdown("""
We now ask you to complete **two short surveys** about your experience.

Thank you for your time!
""")

# Replace with your real Qualtrics survey URLs
survey_1_url = "https://umn.qualtrics.com/jfe/form/SV_51oE0yq20SQ0njg"
survey_2_url = "https://umn.qualtrics.com/jfe/form/SV_51oE0yq20SQ0njg"

# Layout: two columns side by side
left_col, right_col = st.columns(2)

with left_col:
    st.markdown("### 📋 Survey 1")
    st.components.v1.iframe(src=survey_1_url, height=500, width=450, scrolling=True)

with right_col:
    st.markdown("### 📋 Survey 2")
    st.components.v1.iframe(src=survey_2_url, height=500, width=450, scrolling=True)

if st.button("Next"):
    st.session_state.post_surveys_done = True  # ✅ set the flag
    st.switch_page("pages/5_conclusion.py")  

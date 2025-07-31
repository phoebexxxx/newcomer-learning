import streamlit as st

# ✅ Protect this page
if not st.session_state.get("ai_task") or not st.session_state.get("more"):
    st.warning("Please complete the main study before proceeding.")
    st.stop()


st.set_page_config(page_title="Post Task Surveys", layout="wide")
st.title("🧠 Post-Task Surveys")

st.markdown("""
We now ask you to complete **three short surveys** about your experience.
""")

# Replace with your real Qualtrics survey URLs
survey_1_url = "https://umn.qualtrics.com/jfe/form/SV_51oE0yq20SQ0njg"
survey_2_url = "https://umn.qualtrics.com/jfe/form/SV_51oE0yq20SQ0njg"

# Layout: two columns side by side
left_col, right_col = st.columns(2)

with left_col:
    st.markdown("### 📋 Survey 1: Wikipedia knowledge")
    st.components.v1.iframe(src=survey_1_url, height=500, width=450, scrolling=True)

with right_col:
    st.markdown("### 📋 Survey 2: Engagement & Learning")
    st.components.v1.iframe(src=survey_2_url, height=500, width=450, scrolling=True)


st.markdown("### 📋 Survey 3: Interacting with AI")
st.components.v1.iframe(src=survey_2_url, height=500, width=450, scrolling=True)

if st.button("Next"):
    st.session_state.post_surveys_done = True  # ✅ set the flag
    st.switch_page("pages/4_follow_up.py")  

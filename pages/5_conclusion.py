import streamlit as st

st.set_page_config(page_title="Finish & Download", layout="wide")
st.title("🎉 You're All Done!")

st.markdown("""
Thank you for participating in this study.

If you'd like to download a copy of your interaction log, click the button below.
""")

if "logs" in st.session_state and st.session_state.logs:
    log_text = "\n\n".join([f"[{t}] {r.upper()}: {c}" for t, r, c in st.session_state.logs])
    st.download_button("📁 Download Interaction Log", log_text, file_name="interaction_log.txt")
else:
    st.info("No interaction logs found.")

import streamlit as st
import pandas as pd 
import io


if not st.session_state.get("followup_done"): 
    st.warning("Please complete follow up task before you conclude.")
    st.stop()


st.set_page_config(page_title="Finish & Thank you", layout="wide")

st.markdown("""
            
🎉 You are all done! Thank you so much for participating in this study. Again, we truly value your participation. 
            
""")

# if "logs" in st.session_state and st.session_state.logs:
#     log_text = "\n\n".join([f"[{t}] {r.upper()}: {c}" for t, r, c in st.session_state.logs])
#     st.download_button("📁 Download Interaction Log", log_text, file_name="interaction_log.txt")
# else:
#     st.info("No interaction logs found.")


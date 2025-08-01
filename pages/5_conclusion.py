import streamlit as st
import pandas as pd 
import io


if not st.session_state.get("followup_done"): 
    st.warning("Please complete follow up task before you conclude.")
    st.stop()


st.set_page_config(page_title="Finish & Download", layout="wide")
st.title("Download your logs")

st.markdown("""

Before concluding, please make sure to download the logs from the following button, and send to the researcher right now. 
Feel free to keep a copy with you as well.        

""")

if "logs" in st.session_state and st.session_state.logs:
    # Create DataFrame from structured logs
    df = pd.DataFrame(st.session_state.logs)

    # Create in-memory buffer to hold CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    # Download button for CSV
    st.download_button(
        label="📁 Download Interaction Log (CSV)",
        data=csv_buffer.getvalue(),
        file_name="interaction_log.csv",
        mime="text/csv"
    )
else:
    st.info("No interaction logs found.")


st.markdown("""
            
🎉 You are all done! Thank you so much for participating in this study. Again, we truly value your participation. 
            
""")

# if "logs" in st.session_state and st.session_state.logs:
#     log_text = "\n\n".join([f"[{t}] {r.upper()}: {c}" for t, r, c in st.session_state.logs])
#     st.download_button("📁 Download Interaction Log", log_text, file_name="interaction_log.txt")
# else:
#     st.info("No interaction logs found.")


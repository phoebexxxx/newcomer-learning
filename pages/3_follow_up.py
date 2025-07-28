import streamlit as st
import datetime
from streamlit_autorefresh import st_autorefresh

# Optional: Protect this page
# ✅ Protect this page
if not st.session_state.get("sandbox") or not st.session_state.get("count") or st.session_state["count"] < 6:
    st.warning("🚫 Please complete the Main Study task before proceeding.")
    st.stop()

st.set_page_config(page_title="Follow Up", layout="wide")
st.title("🧩 Your Next Wikipedia Task")

def log_event(AorH, component, content):
    st.session_state.logs.append({
        "AorH": AorH,
        "PID": st.session_state["participant_id"], 
        "group": st.session_state["group"],
        "component": component,
        "timestamp": datetime.datetime.now().isoformat(),
        "content": content
    })

st.markdown("""
### 📝 Task Description

Expand the article about **Dutch soccer player Manon Melis** on Wikipedia.  
You can add as **many words, sentences, and references** as you want.  
⏳ You also have as much **time** as you need to complete this task.

🚫 Please **do not** open or read the current Wikipedia article named *Manon Melis*, even if you see it in search results.  
✅ You should gather information from sources **outside of Wikipedia**.

🧠 We encourage you to **think aloud** as you write your contribution.

📄 **Note:** The reference list is simplified.  
You do **not** need to use wikitext — just write in normal text format.

---
""")

st.markdown("### 🧾 Current Stub Article Content")
st.markdown(""" 
<div style='background-color:#f5f5f5; padding:15px; border-radius:8px; overflow-x:auto; width:90%; max-width:700px; font-family: monospace; font-size: 11px; white-space: pre-wrap;'><b>Manon Melis</b> (born 31 August 1986) is a Dutch professional football player who plays as a midfielder in the Damallsvenskan for LdB FC Malmö.
Melis has played for the Netherlands national team since 2005. She played for the Netherlands in the 2007 FIFA Women's World Cup qualifying rounds and the 2010 UEFA Women's Euro finals [1].
<br><b>References</b> 
[1] FIFA players
</div>
""", unsafe_allow_html=True)

# User writing area
st.session_state["follow_up"] = st.text_area(
    label="✏️ Write your expanded content below:",
    height=300,
    key="follow_up_text"
)

# 🔁 Automatically rerun the app every 1 second
st_autorefresh(interval=15000, key="datarefresh")

content = st.session_state.get("follow_up", "").strip()
log_event("human", "taskw/oAI", content)

# When user submits the task
if st.button("✅ Submit Follow-up Task"):
    if content:
        # timestamp = datetime.datetime.now().isoformat()
        # st.session_state.logs.append((timestamp, "follow_up_task", response.strip()))
        log_event("human", "taskw/oAI", content)
        st.success("Your contribution has been saved.")
        st.session_state.followup_done = True
    else:
        st.warning("Please write something before submitting.")

# Show the "Next" button only if task was submitted
if st.session_state.get("followup_done"):
    if st.button("➡️ Next"):
        st.switch_page("pages/4_post_surveys.py")  
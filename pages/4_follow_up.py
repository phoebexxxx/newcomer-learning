import streamlit as st
import datetime
from streamlit_autorefresh import st_autorefresh
from sandbox import follow_sand

# Optional: Protect this page
if not st.session_state.get("post_surveys_done"):
    st.warning("Please complete the post surveys before proceeding.")
    st.stop()

st.set_page_config(page_title="Follow Up", layout="centered")
st.title("🧩 Follow Up Task")

def log_event(AorH, component, content):
    st.session_state.logs.append({
        "AorH": AorH,
        "PID": st.session_state["participant_id"], 
        "group": st.session_state["group"],
        "component": component,
        "timestamp": datetime.datetime.now().isoformat(),
        "content": content
    })


p_id = st.session_state.get("participant_id")
FOLLOW_SAND = follow_sand.follow_sand(int(p_id)-1)

st.markdown("""
### ✍️ Task Description

Now, please improve the article about a Dutch soccer player ***Manon Melis*** on Wikipedia. Your job is to add well-sourced content that fits Wikipedi's standards. 
You can add as many words, sentences, and references as you want. 
            
⏰ **Time limit:** No time limit, recommended 30 minutes
            
**🚫 DON’Ts**
- <u>**DO NOT** use other AI tools </u> like ChatGPT, Claude, Gemini. <u>**DO NOT** look at </u> AI generated summaries.
- <u>**DO NOT open or read**</u> the current Wikipedia article named ***Manon Melis***.  

**✅ DOs**
- You can search for <u>**sources outside of Wikipedia**</u>, and include links for sources if you could.    
- We encourage you to <u>**think aloud**</u> as you write your edits.

---
""", unsafe_allow_html=True)

st.markdown("### 🧾 Current Article Content")
st.markdown(""" 
<div style='background-color:#f5f5f5; padding:15px; border-radius:8px; overflow-x:auto; width:100%; max-width:700px; font-family: monospace; font-size: 11px; white-space: pre-wrap;'><b>Manon Melis</b> (born 31 August 1986) is a Dutch professional football player who plays as a midfielder in the Damallsvenskan for LdB FC Malmö.
Melis has played for the Netherlands national team since 2005. She played for the Netherlands in the 2007 FIFA Women's World Cup qualifying rounds and the 2010 UEFA Women's Euro finals [1].
<br><b>References</b> 
[1] FIFA players
</div>

---
""", unsafe_allow_html=True)

# original sandbox
# # User writing area
# st.session_state["follow_up"] = st.text_area(
#     label="✏️ Write your content below:",
#     height=300,
#     key="follow_up_text"
# )

# # 🔁 Automatically rerun the app every 30 seconds
# st_autorefresh(interval=30000, key="datarefresh")

# content = st.session_state.get("follow_up", "").strip()
# log_event("human", "taskw/oAI", content)

st.markdown("### 📝 Your Editing Sandbox")

st.markdown(
    f"""
    <iframe src="{FOLLOW_SAND}?embedded=true"
            width="100%" height="700" frameborder="0">
    </iframe>
    """,
    unsafe_allow_html=True
)

if st.button("Submit"):
    st.success("Your contribution has been saved.")
    st.session_state.followup_done = True
else: 
    st.warning("Please submit your draft.")


if st.session_state.get("followup_done"):
    st.markdown("""
    ---
    """)
        
    st.markdown("""Please fill out the following short assessment. Each one of them may have <u>one or more</u> correct answer. It tasks around 5 minutes. After you are done with the assessment, please click "Next" to conclude the study.
        """, unsafe_allow_html=True)
    survey_1_url = "https://umn.qualtrics.com/jfe/form/SV_51oE0yq20SQ0njg "
    st.markdown("### 📋 Survey: Wikipedia knowledge")
    st.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <iframe src="{survey_1_url}" width="450" height="700" scrolling="yes" style="border: none;"></iframe>
    </div>
    """,
    unsafe_allow_html=True
    )
    st.markdown("""
    ---
    """)
    if st.button("Next"):
        st.switch_page("pages/5_conclusion.py")  




# original 
# # When user submits the task
# if st.button("Submit"):
#     if content:
#         # timestamp = datetime.datetime.now().isoformat()
#         # st.session_state.logs.append((timestamp, "follow_up_task", response.strip()))
#         log_event("human", "taskw/oAI", content)
#         st.success("Your contribution has been saved.")
#         st.session_state.followup_done = True
#     else:
#         st.warning("Please write something before submitting.")

# # Show the "Next" button only if task was submitted
# if st.session_state.get("followup_done"):
#     if st.button("Next"):
#         st.switch_page("pages/5_conclusion.py")  
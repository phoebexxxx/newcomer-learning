import streamlit as st
import openai
import datetime

# Optional: Protect this page
if not st.session_state.get("participant_id") or not st.session_state.get("group"):
    st.warning("Please complete the Participant Info page first.")
    st.stop()

st.set_page_config(page_title="Wikipedia Assistant", layout="wide")
st.title("Wikipedia Editing Assistant")

#st.set_page_config(page_title="Chat with GPT-4o-mini", page_icon="🤖", layout="wide")

    # Set up the page
    #st.title("Wikipedia Editing Assistant: GPT-4o-mini")

    # Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": """You are a helpful AI assistant for Wikipedia newcomer editors..."""  # Truncated for brevity
    }]
if "logs" not in st.session_state:
    st.session_state.logs = []

# Initialize OpenAI client
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Function to render messages
def render_message(role, content):
    if role == "user":
        st.markdown(
            f"""
            <div style='background-color:#e6f0ff; padding:10px 15px; border-radius:10px; margin:10px 0;'>
                <strong style='color:#0047ab;'>You:</strong><br>{content}
            </div>
            """, unsafe_allow_html=True
        )
    elif role == "assistant":
        st.markdown(
            f"""
            <div style='background-color:#eaffea; padding:10px 15px; border-radius:10px; margin:10px 0;'>
                <strong style='color:#008000;'>GPT:</strong><br>{content}
            </div>
            """, unsafe_allow_html=True
        )

# Layout with two columns
left_col, right_col = st.columns([1.25, 1.25])


# Left column: user editing sandbox
with left_col:
    st.subheader("📝 Your Editing Sandbox")

    st.markdown("### 📌 Task Description")
    st.markdown("""
    The article **Bronwyn Oliver** on Wikipedia is currently a stub, meaning it is short and needs expansion, such that readers can access more information about her.

    **Your task:**  
    Expand this article by adding **150–200 words** and including **at least 3 references** to support the information you add.  
    ⏰ **Time limit:** 25 minutes

    🚫 Please **do not** open or read the current Wikipedia article named *Bronwyn Oliver*, even if you see it in search results.  
    ✅ You should gather information from sources **outside of Wikipedia**.  
    ✍️ Please write your contribution in **wikitext format**. If you're unfamiliar with wikitext, the AI assistant can help you.

    You must have at least **6 interactions** with the AI assistant during the task.  
    One question from you and one answer from the AI count as 1 interaction.

    ---
    """)

    st.markdown("### 🧾 Current Stub Article Content")
    st.markdown("""
    <div style='background-color:#f5f5f5; padding:15px; border-radius:8px; overflow-x:auto; width:90%; max-width:700px; font-family: monospace; font-size: 11px; white-space: pre-wrap;'><b>Bronwyn Oliver</b> (1959–2006) was an Australian sculptor, whose works were primarily made in metal.
    Oliver was born at Gum Flat, west of Inverell, New South Wales, and studied and worked in Sydney.
    Oliver graduated from the College of Fine Arts (COFA), then known as the Alexander Mackie College of Advanced Education in 1980.
    Oliver's major works included Vine, a 16 metre high sculpture installed in the refurbished Sydney Hilton. Her work is held in a range of major collections, including the Art Gallery of New South Wales.
    Oliver committed suicide on 11 July 2006.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✏️ Draft Your Expanded Version")
    
    st.session_state["sandbox"] = st.text_area(
        label="Write your new content or revision in Wikitext here:",
        height=300,
        key="sandbox_input"
    )

    # Submit button
    if st.button("✅ Submit Draft"):
        task_content = st.session_state["sandbox"].strip()

        if task_content:
            timestamp = datetime.datetime.now().isoformat()
            st.session_state.logs.append((timestamp, "task", task_content))
            st.success("✅ Your draft has been submitted and added to logs.")
        else:
            st.warning("Please write something before submitting.")


# Right column: AI interaction
with right_col:

    st.subheader("🤖 Chat with GPT-4o-mini")
    st.write("You are chatting with the `gpt-4o-mini` model via OpenAI API.")

    for message in st.session_state.messages[1:]:  # Skip system message
        render_message(message["role"], message["content"])

    user_input = st.text_area("Enter your prompt:", key="user_input", height=100)

    if st.button("Send"):
        if user_input.strip() == "":
            st.warning("Please enter a prompt.")
        else:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.logs.append(
                (datetime.datetime.now().isoformat(), "user", user_input)
            )

            with st.spinner("GPT-4o-mini is thinking..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=st.session_state.messages
                    )
                    assistant_reply = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
                    st.session_state.logs.append(
                        (datetime.datetime.now().isoformat(), "assistant", assistant_reply)
                    )

                except Exception as e:
                    st.error(f"An error occurred: {e}")

            st.rerun()

# Navigation
if st.session_state["sandbox"].strip() and st.session_state.logs:  # this and is not working
    st.markdown("Please click the button to move on.")
    if st.button("Next"):
        st.switch_page("pages/3_follow_up.py")  
else:
    st.warning("Please complete both fields to continue.")

# Optional: Export logs
with st.expander("📁 Export Logs"):
    if st.session_state.logs:
        log_text = "\n\n".join(
            [f"[{t}] {r.upper()}: {c}" for t, r, c in st.session_state.logs]
        )
        st.download_button("Download Logs as Text File", log_text, file_name="chat_logs.txt")
    else:
        st.write("No logs to export yet.")



# import streamlit as st
# import openai
# import os

# st.set_page_config(page_title="Chat with ScaffoldAI", page_icon="📚")

# st.title("Chat with ScaffoldAI")
# st.write("You are chatting with ScaffoldAI, an AI chatbot powered by LLM.")

# def render_message(role, content):
#     if role == "user":
#         st.markdown(
#             f"""
#             <div style='background-color:#e6f0ff; padding:10px 15px; border-radius:10px; margin:10px 0;'>
#                 <strong style='color:#0047ab;'>You:</strong><br>{content}
#             </div>
#             """, unsafe_allow_html=True
#         )
#     elif role == "assistant":
#         st.markdown(
#             f"""
#             <div style='background-color:#eaffea; padding:10px 15px; border-radius:10px; margin:10px 0;'>
#                 <strong style='color:#008000;'>GPT:</strong><br>{content}
#             </div>
#             """, unsafe_allow_html=True
#         )


# # Set secert key 
# client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])



# # System prompt for scaffolding but no RAG (defines the bot’s behavior)
# # system_prompt = """You are a helpful AI assistant for Wikipedia newcomer editors. Your primary goal is to support learning through active engagement and granular level of information. When a newcomer asks a question or requests help, respond by guiding them rather than doing the task for them. 

# # When the newcomer asks a question before they make any attempts, first articulate user intent, so that you have a clear idea about the user’s [task] for an article about [topic]. Then retrieval from Wikipedia policies pages regarding this type of edit. For example, if the topic is biographies, you may want to talk about Manual of style/biography and biographies of living persons. 

# # If the task the newcomer wants to work on is too complex for their current skill level, for example, creating an article from scratch or expanding a stub article (you can refer to this page: https://en.wikipedia.org/wiki/Wikipedia:Task_Center for the difficulty level of tasks), break it down into smaller, achievable steps, and prompt them to take actions. 

# # When a newcomer makes some attempts and asks for feedback, use your retrieval capabilities to simulate community response by referencing relevant Wikipedia content policies (e.g., Neutral point of view, Verifiability, No original research). Please also consider user intent again, and retrieve more relevant and specific to the particular topic that newcomers are working on. Provide responses from diverse perspectives such as experienced editors, readers, and/or other newcomer editors. 

# # Once the newcomer finishes a task, provide a reflective summary of what they did and what they learned, along with encouragement to continue contributing. 

# # DO NOT DIRECTLY perform tasks or provide complete answers, unless newcomers have already attempted to make edits, expressed clear frustration of being stuck, or ask explicitly for an example. Even when newcomers try to ask for example, do not directly give answers about the topic they are editing, but some examples that are along similar topics. 
# # Prioritize participation, engagement, and reflection. You can reject their question softly by saying you can't. 

# # Since you are interacting with newcomers, they might be overwhelmed by too much information at once, so try to be general, short and precise. DO NOT give too much information to newcomers each round of interaction.

# # """



# # System prompt for scaffolding and RAG (defines the bot's behavior)
# system_prompt = """You are a helpful AI assistant for Wikipedia newcomer editors. Your primary goal is to support learning through active engagement and granular level of information. When a newcomer asks a question or requests help, respond by guiding them rather than doing the task for them. 

# When the newcomer asks a question before they make any attempts, first articulate user intent, so that you have a clear idea about the user’s [task] for an article about [topic]. Then retrieval from Wikipedia policies pages regarding this type of edit. For example, if the topic is biographies, you may want to talk about Manual of style/biography and biographies of living persons. 

# If the task the newcomer wants to work on is too complex for their current skill level, for example, creating an article from scratch or expanding a stub article (you can refer to this page: https://en.wikipedia.org/wiki/Wikipedia:Task_Center for the difficulty level of tasks), break it down into smaller, achievable steps, and prompt them to take actions. 

# When a newcomer makes some attempts and asks for feedback, use your retrieval capabilities to simulate community response by referencing relevant Wikipedia content policies (e.g., Neutral point of view, Verifiability, No original research). Please also consider user intent again, and retrieve more relevant and specific to the particular topic that newcomers are working on. Provide responses from diverse perspectives such as experienced editors, readers, and/or other newcomer editors. 

# Once the newcomer finishes a task, provide a reflective summary of what they did and what they learned, along with encouragement to continue contributing. 

# DO NOT DIRECTLY perform tasks or provide complete answers, unless newcomers have already attempted to make edits, expressed clear frustration of being stuck, or ask explicitly for an example. Even when newcomers try to ask for example, do not directly give answers about the topic they are editing, but some examples that are along similar topics. 
# Prioritize participation, engagement, and reflection. You can reject their question softly by saying you can't. 

# Since you are interacting with newcomers, they might be overwhelmed by too much information at once, so try to be short and precise. DO NOT give too much information to newcomers each round of interaction.

# You have access to the following Wikipedia policy pages and should use them when relevant. Please provide the sources you used to newcomers:
# - https://en.wikipedia.org/wiki/Wikipedia:Notability
# - https://en.wikipedia.org/wiki/Wikipedia:Notability_(people)#Creative_professionals
# - https://en.wikipedia.org/wiki/Wikipedia:Biographies_of_living_persons
# - https://en.wikipedia.org/wiki/Wikipedia:Conflict_of_interest
# - https://en.wikipedia.org/wiki/Wikipedia:Verifiability
# - https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources
# - https://en.wikipedia.org/wiki/Wikipedia:No_original_research
# - https://en.wikipedia.org/wiki/Wikipedia:Neutral_point_of_view
# - https://en.wikipedia.org/wiki/Wikipedia:NPOV_tutorial
# """



# # Commonly used roles include “system,” “user,” and “assistant.” 
# # The “system” provides high-level instructions, the “user” presents queries or prompts, 
# # and the “assistant” is the model’s response. 
# # By differentiating these roles, we can set the context and direct the conversation efficiently.

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = [{"role": "system", "content": system_prompt}]

# # Display chat history
# for message in st.session_state.messages:
#     render_message(message["role"], message["content"])
# # for message in st.session_state.messages[1:]:  # skip system message
# #     if message["role"] == "user":
# #         st.markdown(f"**You:** {message['content']}")
# #     elif message["role"] == "assistant":
# #         st.markdown(f"**GPT-4o-mini:** {message['content']}")

# # Input box
# user_input = st.text_input("Enter your prompt:", key="user_input")

# if st.button("Send"):
#     if user_input.strip() == "":
#         st.warning("Please enter a prompt.")
#     else:
#         # Append user message
#         st.session_state.messages.append({"role": "user", "content": user_input})
#         print(st.session_state.messages)
#         print("/n")
#         print("/n")

#         with st.spinner("GPT-4o-mini is thinking..."):
#             try:
#                 response = client.chat.completions.create(
#                     model="gpt-4o-mini",  # can change model here
#                     messages=st.session_state.messages
#                 )
#                 # print(response)
#                 # print("/n")
#                 # print("/n")
#                 assistant_reply = response.choices[0].message.content
#                 # print(assistant_reply)
#                 # print("/n")
#                 # print("/n")
#                 st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

#             except Exception as e:
#                 st.error(f"An error occurred: {e}")

#         st.rerun()




# import streamlit as st
# import openai
# import os
# import requests

# st.set_page_config(page_title="Chat with ScaffoldAI", page_icon="📚")

# st.title("Chat with ScaffoldAI")
# st.write("You are chatting with ScaffoldAI, an AI chatbot powered by LLM.")

# # Render formatted messages
# def render_message(role, content):
#     if role == "user":
#         st.markdown(
#             f"""
#             <div style='background-color:#e6f0ff; padding:10px 15px; border-radius:10px; margin:10px 0;'>
#                 <strong style='color:#0047ab;'>You:</strong><br>{content}
#             </div>
#             """, unsafe_allow_html=True
#         )
#     elif role == "assistant":
#         st.markdown(
#             f"""
#             <div style='background-color:#eaffea; padding:10px 15px; border-radius:10px; margin:10px 0;'>
#                 <strong style='color:#008000;'>GPT:</strong><br>{content}
#             </div>
#             """, unsafe_allow_html=True
#         )

# # Set OpenAI secret key
# client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# # Wikipedia policy titles
# POLICY_TITLES = {
#     "Notability": "Wikipedia:Notability",
#     "Creative Professionals": "Wikipedia:Notability_(people)",
#     "BLP": "Wikipedia:Biographies_of_living_persons",
#     "COI": "Wikipedia:Conflict_of_interest",
#     "Verifiability": "Wikipedia:Verifiability",
#     "Reliable Sources": "Wikipedia:Reliable_sources",
#     "No Original Research": "Wikipedia:No_original_research",
#     "Neutral Point of View": "Wikipedia:Neutral_point_of_view",
#     "NPOV Tutorial": "Wikipedia:NPOV_tutorial"
# }

# # Fetch Wikipedia plain text content
# def fetch_wikipedia_text(title):
#     url = f"https://en.wikipedia.org/api/rest_v1/page/plain/{title}"
#     headers = {'User-Agent': 'ScaffoldAI/1.0'}
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         return response.text
#     else:
#         return f"Failed to retrieve content for: {title}"

# # Retrieve relevant policy chunks based on user input
# def retrieve_relevant_policies(user_query, policy_docs):
#     relevant_snippets = []
#     for policy_name, text in policy_docs.items():
#         if any(word.lower() in text.lower() for word in user_query.split()):
#             snippet = text[:1000]  # Simplified first-1k-char chunk
#             relevant_snippets.append(f"=== {policy_name} ===\n{snippet}")
#     return "\n\n".join(relevant_snippets[:3])

# # Define system prompt
# system_prompt = """You are a helpful AI assistant designed specifically to support newcomer editors on Wikipedia. Your primary goal is to foster learning by guiding newcomers through active engagement, rather than doing editing tasks for them. Prioritize scaffolded instruction, policy awareness, and community-aligned reasoning. 
# When a newcomer first asks a question or requests help, always begin by clarifying their intent: what is their [task] and [topic] for the [article] they want to work on? If they include it in their query, do not ask again. 
# DO NOT perform the task for them unless they’ve already made an attempt. Even then, guide rather than solve. 
# If a newcomer’s task is complex (e.g. starting a new article or expanding a stub), break it down to smaller, achievable, beginner-friendly steps. This is important for scaffolding. Ask them to take action before giving more feedback. 
# Retrieve relevant Wikipedia policy and guideline pages based on the user's topic and task. Some specific policy links that might be helpful. Please be sure to provide the actual links to relevant policy pages for the newcomers to click and read. 
# https://en.wikipedia.org/wiki/Wikipedia:Content_assessment 
# https://en.wikipedia.org/wiki/Wikipedia:Notability 
# https://en.wikipedia.org/wiki/Wikipedia:Notability_(people)#Creative_professionals  
# https://en.wikipedia.org/wiki/Wikipedia:Biographies_of_living_persons 
# https://en.wikipedia.org/wiki/Wikipedia:Conflict_of_interest 
# https://en.wikipedia.org/wiki/Wikipedia:Verifiability 
# https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources 
# https://en.wikipedia.org/wiki/Wikipedia:No_original_research
# https://en.wikipedia.org/wiki/Wikipedia:Neutral_point_of_view 
# https://en.wikipedia.org/wiki/Wikipedia:NPOV_tutorial 
# When a newcomer makes an attempt (e.g., writes content, finds a source, drafts a sentence), respond with constructive feedback. Simulate responses from the Wikipedia community by referencing how experienced editors might respond using relevant content guidelines and policies.
# Once the newcomer finishes a task, provide a reflective summary of what they did and what they learned, along with encouragement to continue contributing. 
# """

# # Initialize chat session
# if "messages" not in st.session_state:
#     st.session_state.messages = [{"role": "system", "content": system_prompt}]
#     st.session_state.policy_docs = {
#         key: fetch_wikipedia_text(title) for key, title in POLICY_TITLES.items()
#     }

# # Render chat history
# for message in st.session_state.messages:
#     render_message(message["role"], message["content"])

# # Text input
# user_input = st.text_input("Enter your prompt:", key="user_input")

# if st.button("Send"):
#     if user_input.strip() == "":
#         st.warning("Please enter a prompt.")
#     else:
#         st.session_state.messages.append({"role": "user", "content": user_input})

#         # Retrieve relevant policy context
#         retrieved_context = retrieve_relevant_policies(user_input, st.session_state.policy_docs)
#         if retrieved_context:
#             st.session_state.messages.insert(
#                 1,
#                 {"role": "system", "content": f"Relevant policy context:\n{retrieved_context}"}
#             )

#         with st.spinner("GPT-4o-mini is thinking..."):
#             try:
#                 response = client.chat.completions.create(
#                     model="gpt-4o-mini",
#                     messages=st.session_state.messages
#                 )
#                 assistant_reply = response.choices[0].message.content
#                 st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
#             except Exception as e:
#                 st.error(f"An error occurred: {e}")

#         st.rerun()


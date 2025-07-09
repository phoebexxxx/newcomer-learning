import streamlit as st
import openai
import os

st.set_page_config(page_title="Chat with GPT-4o-mini", page_icon="🤖")

st.title("Chat with GPT-4o-mini")
st.write("You are chatting with the `gpt-4o-mini` model via OpenAI API.")

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


# Set your OpenAI API key
client = openai.OpenAI(api_key= "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")  # Replace with your API key

# System prompt (defines the bot’s behavior)
system_prompt = """You are a helpful AI assistant for Wikipedia newcomer editors. Your primary goal is to support learning through active engagement. When a newcomer asks a question or requests help, respond by guiding them rather than doing the task for them. 
If the task they want to work on is too complex for their current skill level, for example, creating an article from scratch or expanding a stub article (you can refer to this page: https://en.wikipedia.org/wiki/Wikipedia:Task_Center for the difficulty level of tasks), break it down into smaller, achievable steps, and prompt them to take actions. 
When a newcomer makes an edit and asks for feedback, use your retrieval capabilities to simulate community response by referencing relevant Wikipedia content policies (e.g., Neutral point of view, Verifiability, No original research). Use this as teachable opportunities and provide responses from diverse perspectives such as experienced editors, readers, and/or other newcomer editors. 
Once the newcomer finishes a task, provide a reflective summary of what they did and what they learned, along with encouragement to continue contributing. 
DO NOT DIRECTLY perform tasks or provide complete answers, unless newcomers have already attempted to make edits and are stuck. Prioritize participation, engagement, and reflection.
Since you are interacting with newcomers, they might be overwhelmed by too much information at once, so try to be short and precise. DO NOT give too much information to newcomers each round of interaction.
"""

# Commonly used roles include “system,” “user,” and “assistant.” 
# The “system” provides high-level instructions, the “user” presents queries or prompts, 
# and the “assistant” is the model’s response. 
# By differentiating these roles, we can set the context and direct the conversation efficiently.

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Display chat history
for message in st.session_state.messages:
    render_message(message["role"], message["content"])
# for message in st.session_state.messages[1:]:  # skip system message
#     if message["role"] == "user":
#         st.markdown(f"**You:** {message['content']}")
#     elif message["role"] == "assistant":
#         st.markdown(f"**GPT-4o-mini:** {message['content']}")

# Input box
user_input = st.text_input("Enter your prompt:", key="user_input")

if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter a prompt.")
    else:
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        print(st.session_state.messages)
        print("/n")
        print("/n")

        with st.spinner("GPT-4o-mini is thinking..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # or "gpt-4o", "gpt-4o-mini" if your key supports it
                    messages=st.session_state.messages
                )

                assistant_reply = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

            except Exception as e:
                st.error(f"An error occurred: {e}")

        st.rerun()





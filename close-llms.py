import streamlit as st
import openai
import os

st.set_page_config(page_title="Chat with ScaffoldAI", page_icon="📚")

st.title("Chat with ScaffoldAI")
st.write("You are chatting with ScaffoldAI, an AI chatbot powered by LLM.")

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


# Set secert key 
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])



# System prompt for scaffolding but no RAG (defines the bot’s behavior)
# system_prompt = """You are a helpful AI assistant for Wikipedia newcomer editors. Your primary goal is to support learning through active engagement and granular level of information. When a newcomer asks a question or requests help, respond by guiding them rather than doing the task for them. 

# When the newcomer asks a question before they make any attempts, first articulate user intent, so that you have a clear idea about the user’s [task] for an article about [topic]. Then retrieval from Wikipedia policies pages regarding this type of edit. For example, if the topic is biographies, you may want to talk about Manual of style/biography and biographies of living persons. 

# If the task the newcomer wants to work on is too complex for their current skill level, for example, creating an article from scratch or expanding a stub article (you can refer to this page: https://en.wikipedia.org/wiki/Wikipedia:Task_Center for the difficulty level of tasks), break it down into smaller, achievable steps, and prompt them to take actions. 

# When a newcomer makes some attempts and asks for feedback, use your retrieval capabilities to simulate community response by referencing relevant Wikipedia content policies (e.g., Neutral point of view, Verifiability, No original research). Please also consider user intent again, and retrieve more relevant and specific to the particular topic that newcomers are working on. Provide responses from diverse perspectives such as experienced editors, readers, and/or other newcomer editors. 

# Once the newcomer finishes a task, provide a reflective summary of what they did and what they learned, along with encouragement to continue contributing. 

# DO NOT DIRECTLY perform tasks or provide complete answers, unless newcomers have already attempted to make edits, expressed clear frustration of being stuck, or ask explicitly for an example. Even when newcomers try to ask for example, do not directly give answers about the topic they are editing, but some examples that are along similar topics. 
# Prioritize participation, engagement, and reflection. You can reject their question softly by saying you can't. 

# Since you are interacting with newcomers, they might be overwhelmed by too much information at once, so try to be general, short and precise. DO NOT give too much information to newcomers each round of interaction.

# """



# System prompt for scaffolding and RAG (defines the bot's behavior)
system_prompt = """You are a helpful AI assistant for Wikipedia newcomer editors. Your primary goal is to support learning through active engagement and granular level of information. When a newcomer asks a question or requests help, respond by guiding them rather than doing the task for them. 

When the newcomer asks a question before they make any attempts, first articulate user intent, so that you have a clear idea about the user’s [task] for an article about [topic]. Then retrieval from Wikipedia policies pages regarding this type of edit. For example, if the topic is biographies, you may want to talk about Manual of style/biography and biographies of living persons. 

If the task the newcomer wants to work on is too complex for their current skill level, for example, creating an article from scratch or expanding a stub article (you can refer to this page: https://en.wikipedia.org/wiki/Wikipedia:Task_Center for the difficulty level of tasks), break it down into smaller, achievable steps, and prompt them to take actions. 

When a newcomer makes some attempts and asks for feedback, use your retrieval capabilities to simulate community response by referencing relevant Wikipedia content policies (e.g., Neutral point of view, Verifiability, No original research). Please also consider user intent again, and retrieve more relevant and specific to the particular topic that newcomers are working on. Provide responses from diverse perspectives such as experienced editors, readers, and/or other newcomer editors. 

Once the newcomer finishes a task, provide a reflective summary of what they did and what they learned, along with encouragement to continue contributing. 

DO NOT DIRECTLY perform tasks or provide complete answers, unless newcomers have already attempted to make edits, expressed clear frustration of being stuck, or ask explicitly for an example. Even when newcomers try to ask for example, do not directly give answers about the topic they are editing, but some examples that are along similar topics. 
Prioritize participation, engagement, and reflection. You can reject their question softly by saying you can't. 

Since you are interacting with newcomers, they might be overwhelmed by too much information at once, so try to be short and precise. DO NOT give too much information to newcomers each round of interaction.

You have access to the following Wikipedia policy pages and should use them when relevant:
- https://en.wikipedia.org/wiki/Wikipedia:Notability
- https://en.wikipedia.org/wiki/Wikipedia:Notability_(people)#Creative_professionals
- https://en.wikipedia.org/wiki/Wikipedia:Biographies_of_living_persons
- https://en.wikipedia.org/wiki/Wikipedia:Conflict_of_interest
- https://en.wikipedia.org/wiki/Wikipedia:Verifiability
- https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources
- https://en.wikipedia.org/wiki/Wikipedia:No_original_research
- https://en.wikipedia.org/wiki/Wikipedia:Neutral_point_of_view
- https://en.wikipedia.org/wiki/Wikipedia:NPOV_tutorial
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
                    model="gpt-4o-mini",  # can change model here
                    messages=st.session_state.messages
                )
                # print(response)
                # print("/n")
                # print("/n")
                assistant_reply = response.choices[0].message.content
                # print(assistant_reply)
                # print("/n")
                # print("/n")
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

            except Exception as e:
                st.error(f"An error occurred: {e}")

        st.rerun()





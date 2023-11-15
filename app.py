import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key= os.getenv("OPENAI_API_KEY"),
)

def get_session_state():
    session_state = st.session_state
    if 'first_time' not in session_state:
        session_state.first_time = True
    return session_state

session_state = get_session_state()
print(session_state)
if session_state.first_time:
    print('executed')
    #Create an assistant. Uncomment the below code for the first time then comment it because we dont want to create assistant every-time.

    # assistant = client.beta.assistants.create(
    # instructions="You are a customer support chatbot. Use your knowledge base to best respond to customer queries.",
    # model="gpt-4-1106-preview",
    # tools=[{"type": "retrieval"}]
    # )
    

    #Initializing a thread
    thread = client.beta.threads.create()
    session_state.thread_id = thread.id
    session_state.assistant_id = "asst_QZiMHSTvtm7GdS2CCli6FfKJ"
    session_state.first_time = False

user_input = st.text_input(label= "Enter something:",placeholder= "Type here...")

def create_message(query,thread_id):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content= query
    )

def bot_response(thread_id,assistant_id):
    run = client.beta.threads.runs.create(
    thread_id = thread_id,
    assistant_id = assistant_id
    )
    while True:
        run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run.id
        )
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            latest_message = messages.data[0]
            text = latest_message.content[0].text.value
            break
    return text


if st.button("Submit"):
    st.write("User:",user_input)
    with st.spinner("Processing"):
        thread_id = session_state.thread_id 
        assistant_id = session_state.assistant_id 
        print(assistant_id)
        print(thread_id)
        message = create_message(user_input,thread_id)
        text = bot_response(thread_id,assistant_id)
        st.write(text)



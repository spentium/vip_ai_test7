import streamlit as st
from openai import OpenAI
import time

MODEL_LIST = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o"]
assistant_id = "asst_Dlr6YRJen7llwFxT393E5noC"

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

    client = OpenAI(api_key=openai_api_key)

    thread_id = st.text_input("Thread ID")
    thread_btn = st.button("Create a new thread")

    if thread_btn:
        thread = client.beta.threads.create()
        thread_id = thread.id
    
        st.subheader(f"{thread_id}")
        st.info("Thread created!")

st.title("💬 VIP AI")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "저는 AI 인턴입니다. 무엇이든지 시켜주시면, 최선을 다해 답변드리겠습니다."}]

model: str = st.selectbox("Model", options=MODEL_LIST)  # type: ignore

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if not thread_id:
        st.info("Please add your Thread ID to continue.")
        st.stop()
        
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=prompt
        )
    
    run = client.beta.threads.runs.create(
        thread_id = thread_id,
        assistant_id = assistant_id,
        model = model
        )

    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id = thread_id,
            run_id = run_id,
            model = model
            )
        if run.status == "completed":
            break
        else:
            time.sleep(2)

    thread_messages = client.beta.threads.messages.list(thread_id)
    msg = thread_messages.data[0].content[0].text.value

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

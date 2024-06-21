import streamlit as st
from openai import OpenAI
import time

assistant_id = "asst_Dlr6YRJen7llwFxT393E5noC"

# 사이드바에서 OpenAI API 키와 Thread ID 입력 받기
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    client = OpenAI(api_key=openai_api_key)
    thread_id = st.text_input("Thread ID")
    thread_btn = st.button("Create a new thread")

    if thread_btn:
        thread_id = thread.id
        st.subheader(f"{thread_id}")
        st.info("Thread created!")

st.title("💬 VIP AI")

# 세션 상태에 메시지 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "저는 AI 인턴입니다. 무엇이든지 시켜주시면, 최선을 다해 답변드리겠습니다."}]

# 메시지 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 파일 업로드 기능 추가
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type, "filesize": uploaded_file.size}
    st.write(file_details)
    st.session_state["messages"].append({"role": "user", "content": f"Uploaded file: {uploaded_file.name}"})
    st.chat_message("user").write(f"Uploaded file: {uploaded_file.name}")

# 사용자 입력 받기
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if not thread_id:
        st.info("Please add your Thread ID to continue.")
        st.stop()

    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=prompt,
        model="gpt-4o"
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        model="gpt-4o"
    )

    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        if run.status == "completed":
            break
        else:
            time.sleep(2)

    thread_messages = client.beta.threads.messages.list(thread_id)
    msg = thread_messages.data[0].content[0].text.value

    st.session_state["messages"].append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)


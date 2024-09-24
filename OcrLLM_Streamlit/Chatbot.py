from openai import OpenAI
import streamlit as st

with st.sidebar:
    "[View the source code](https://github.com/xzhou42/OcrLLM/tree/main/OcrLLM_Streamlit)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/xzhou42/OcrLLM/tree/main/contract-recog)"

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Local Ollama")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "今天我能帮你做什么?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key='ollama',  # api_key没用，应该是随便填
    )
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("加载中"):
        response = client.chat.completions.create(model="qwen2", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

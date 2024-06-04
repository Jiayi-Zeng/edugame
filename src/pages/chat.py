import streamlit as st
from openai import OpenAI
from utils import get_from_url_param, get_api_key
import config.prompt as prompt
import os

param_value = get_from_url_param('knowledge')

st.header(f"知识点: {param_value}")

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": prompt.instruction}, {"role": "assistant", "content": prompt.starter}]
   
for msg in st.session_state["messages"]:
    if msg["role"] in ["user", "assistant"]:
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
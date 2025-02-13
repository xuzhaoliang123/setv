import os
import time
import streamlit as st
import qianfan

os.environ["QIANFAN_ACCESS_KEY"] = "ALTAKM4XAewqxtitZrrlcfAwGf"
os.environ["QIANFAN_SECRET_KEY"] = "273e3e8fe2344512b905090fb4441e87"

# 初始化聊天补全对象
chat_comp = qianfan.ChatCompletion()

def main_page():

    st.title("和机器人BIN聊天吧")
    # 如果没有历史会话则初始化“你好，请问有什么问题吗？”
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state["messages"].append({"role": "assistant", "content": "你好，请问有什么问题吗？"})
    # 有会话就输入会话
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    # 使用chat_input函数获取用户的输入，并将其存储在变量prompt中。如果用户输入了内容，条件判断为真。
    if prompt := st.chat_input():
        # 把输入添加到message中
        st.session_state.messages.append({"role": "user", "content": prompt})
        # 显示在界面中
        with st.chat_message("user"):
            st.markdown(prompt)
        # 使用chat_comp生成回复，丢弃第一句话（欢迎话）
        resp = chat_comp.do(model="ERNIE-3.5-8K", messages=st.session_state.messages[1:], stream=True)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for r in resp:
                chunk = r["body"]["result"]
                full_response += chunk
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        msg = full_response
        # 把回复添加到message中
        st.session_state.messages.append({"role": "assistant", "content": msg})

if __name__ == '__main__':
    main_page()
import streamlit as st
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory

from helpers import page
from prompt import System_prompt
from utils import  get_ai_chat_stream
from database import get_chat_ids

if page():
    st.title("AI助手聊天")
    if 'chat_id' not in st.session_state:
        st.session_state['chat_id'] = ""
        st.session_state['message'] = [{"role": "ai",
                                        "content": "你好！我是你的编程学习助手。我可以帮你解答编程相关的问题，或者提供编程学习的建议。请问你有什么问题吗？"}]


    user_id = st.session_state.get('user_info', {}).get('id', None)
    new_chat_id = st.text_input("输入聊天 ID")

    if new_chat_id != st.session_state['chat_id']:
        st.session_state['chat_id'] = new_chat_id
        st.session_state['message'] = [{"role": "ai", "content": "你好！我是你的编程学习助手。我可以帮你解答编程相关的问题，或者提供编程学习的建议。请问你有什么问题吗？"}]
    session_id = f"{user_id} + {new_chat_id}"
    config = {"configurable": {"session_id": session_id}}
    question = st.chat_input("输入聊天内容")

    for message in st.session_state['message']:
        st.chat_message(message['role']).write(message['content'])

    if question:
        st.session_state['message'].append({"role": "user", "content": question})
        st.chat_message("user").write(question)
        with st.spinner("AI 正在思考"):
            ai_response_placeholder = st.empty()
            response = get_ai_chat_stream(question, session_id, ai_response_placeholder)
            st.session_state['message'].append({"role": "ai", "content": response})
    if user_id:
        chat_ids = get_chat_ids(user_id)
        st.sidebar.title("已有的聊天ID")
        if chat_ids:
            chat_ids_html = "\n".join([f"<li>{chat_id}</li>" for chat_id in chat_ids])
            st.sidebar.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; background-color: #000;">
                    <ul style="list-style-type: disc; margin: 0; padding-left: 20px;">
                        {chat_ids_html}
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.sidebar.write("没有找到聊天记录")

else:
    st.title("请先登录！")
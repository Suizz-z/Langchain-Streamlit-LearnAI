import streamlit as st
from database import init_db

init_db()

pages = {
    "首页": [
        st.Page("Login_Registration.py", title="登陆与注册"),
    ],
    "专项学习": [
        st.Page("Study_tree.py", title="知识图谱"),
        st.Page("Study_node.py", title="知识点学习"),
    ],
    "AI个性化学习": [
        st.Page("AI_conversations.py", title="AI助手"),
    ],
    "习题练习": [
        st.Page("Generate_exercises.py", title="生成练习题"),
        st.Page("History_topics.py", title="答题记录"),
    ],
}

pg = st.navigation(pages)
pg.run()
from database import get_user_history,get_user_history_times
from helpers import page
import streamlit as st
if page():
    st.subheader("历史答题记录")
    user_id = st.session_state['user_info']['id']
    history_times = get_user_history_times(user_id)
    selected_time = st.selectbox("选择时间", history_times)
    if st.button("显示历史答题记录"):
        history = get_user_history(user_id, selected_time)
        if history:
            st.write(f"以下是 {selected_time} 的历史答题记录：")
            for record in history:
                st.write(f"时间: {record[0]}, 问题: {record[1]}")
        else:
            st.write(f"没有找到 {selected_time} 的历史答题记录。")
else:
    st.title("请先登录！")
import streamlit as st
from database import add_user, check_user
from  utils import  summarize_learning_status_streamlit


st.set_page_config(
    page_title="AI编程学习助手",
    page_icon="💻",
    layout="centered"
)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = None
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

st.title("AI编程学习助手💻")

st.markdown("<br/><br/>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")

with col1:
    st.subheader("登陆")
    login_username = st.text_input("请输入用户名", key="login_username")
    login_password = st.text_input("输入密码", type="password", key="login_password")
    if st.button("登录"):
        if login_username and login_password:
            user_info =  check_user(login_username, login_password)
            if user_info:
                st.success("登录成功！")
                st.session_state['logged_in'] = True
                st.session_state['user_info'] = {
                    'id': user_info[0],
                    'username': user_info[1]
                }
                user_id = st.session_state['user_info']['id']
            else:
                st.error("用户名或密码错误。")
        else:
            st.error("请输入用户名和密码")

with col2:
    st.subheader("注册成为新用户")
    signup_username = st.text_input("请输入用户名", key="signup_username")
    signup_password = st.text_input("输入密码", type="password", key="signup_password")
    useremail = st.text_input("请输入邮箱", key="useremail")
    if st.button("提交注册"):
        if signup_username and signup_password and useremail:
            if add_user(signup_username, signup_password, useremail):
                st.success("注册成功🎉")
            else:
                st.error("用户名或邮箱已存在，请重试。")
        else:
            st.error("请输入完整信息")

if st.session_state['logged_in']:
    st.write(f"欢迎回来，{st.session_state['user_info']['username']}！")
    if st.button("注销"):
        st.session_state['logged_in'] = False
    st.divider()
    st.header("近期学习总结")
    summary_placeholder = st.empty()
    summary_placeholder.write("正在生成总结，请稍候...")
    summarize_learning_status_streamlit(st.session_state['user_info']['id'],summary_placeholder)
from datetime import datetime
import streamlit as st
from database import add_user_question
from helpers import page, parse_questions
from utils import generate_practice_questions, generate_learning_path

if page():
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = [None]

    st.title("AI 练习题生成器")

    # 练习题生成表单
    with st.form("create_question"):
        language = st.selectbox("选择你想要学习的编程语言:", ["Python", "JavaScript", "Java", "C++", "C#"])
        mode = st.selectbox("选择你的学习水平:", ["初学者", "中级", "高级"])
        completed_topics = st.text_input("输入你想学习的案例（用逗号分隔）:")
        question_types = st.multiselect("选择你想要的题目类型:", ["选择题", "判断题", "填空题"])
        num_questions = st.number_input("输入你想要的题目数量:", min_value=1, max_value=10, value=5)

        if 'practice_questions' not in st.session_state:
            st.session_state.practice_questions = None

        completed_topics = completed_topics.split(",") if completed_topics else []

        submit = st.form_submit_button("生成练习题")

    if submit:
        with st.spinner("AI正在思考"):
            practice_questions = generate_practice_questions(
                language,
                mode,
                completed_topics,
                num_questions,
                question_types
            )
            st.session_state.practice_questions = parse_questions(practice_questions)
            st.session_state.user_answers = [None] * len(st.session_state.practice_questions)

    # 显示题目和答案输入
    if st.session_state.practice_questions:
        with st.form("submit_answer"):
            for i, question in enumerate(st.session_state.practice_questions):
                if question['type'] == "选择题":
                    st.session_state.user_answers[i] = st.radio(
                        f"{question['question']}",
                        question['options'],
                        index=0 if st.session_state.user_answers[i] is None
                        else question['options'].index(st.session_state.user_answers[i])
                    )
                elif question['type'] == "判断题":
                    st.session_state.user_answers[i] = st.radio(
                        f"{question['question']}",
                        question['options'],
                        index=0 if st.session_state.user_answers[i] is None
                        else question['options'].index(st.session_state.user_answers[i])
                    )
                elif question['type'] == "填空题":
                    st.session_state.user_answers[i] = st.text_input(
                        question['question']
                    )
            st.form_submit_button("提交答案")

    if st.button("分析答案") and 'user_answers' in st.session_state:
        analysis_placeholder = st.empty()  # 创建独立输出容器
        analysis_placeholder.markdown("")  # 清空可能残留的内容

        with st.spinner("AI正在分析答案"):
            # 调用修改后的generate_learning_path并传入专属占位符
            analyse = generate_learning_path(
                st.session_state.practice_questions,
                st.session_state.user_answers,
                analysis_placeholder  # 新增参数传递
            )

            analysis_placeholder.markdown(analyse)


        user_id = st.session_state.get('user_info', {}).get('id', None)
        if user_id:
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            add_user_question(user_id, current_date, str(analyse))
        else:
            st.warning("用户未登录，无法保存历史题目。")
else:
    st.title("请先登录！")

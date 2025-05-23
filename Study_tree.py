from d3blocks import D3Blocks
import json
import pandas as pd
import streamlit as st
from utils import get_ai_tree
from database import load_tree_data, save_tree_data
import streamlit.components.v1 as components
from helpers import page

if page():

    st.markdown(
        """
        <style>
        .st-emotion-cache-13ln4jf {
            max-width: 80% !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    d3 = D3Blocks(verbose='info', chart='tree', frame=False)

    if 'ct' not in st.session_state:
        st.session_state.ct = None
    if 'tree_node_properties' not in st.session_state:
        st.session_state.tree_node_properties = None
    if 'tree_name' not in st.session_state:
        st.session_state.tree_name = None
    if 'first_tree' not in st.session_state:
        st.session_state.first_tree = True

    language = st.selectbox("选择你想要学习的编程语言:", ["Python", "JavaScript", "Java", "C++", "C#"])
    user_id = st.session_state.get('user_info', {}).get('id', None)
    tree_name = f"tree_for_{language}"
    st.session_state.tree_name = tree_name

    df, node_properties = load_tree_data(user_id, tree_name)

    if df is None and node_properties is None:
        st.session_state.first_tree = True
    else:
        st.session_state.first_tree = False

    first = st.session_state.first_tree

    if first:
        submit = st.button("生成文案")

        if submit:
            res = get_ai_tree(language, subject=language)
            data = res.content
            data_dict = json.loads(data)
            df = pd.DataFrame(data_dict)

            d3.set_node_properties(df)
            st.session_state.ct = df
            st.session_state.tree_node_properties = d3.node_properties

            save_tree_data(user_id, tree_name, df, d3.node_properties)

            st.success("新树已创建并保存到数据库。")
    else:
        st.session_state.ct = df
        st.session_state.tree_node_properties = node_properties
        st.write("已加载数据库中的树。")

    create_tree = st.button("显示树", disabled=first)

    if create_tree:
        df = st.session_state.ct
        if df is not None:
            d3.node_properties = st.session_state.tree_node_properties
            html_content = d3.tree(
                df,
                hierarchy=[1, 2, 3, 4, 5, 6, 7, 8],
                figsize=(1000, 1000),
                filepath=None,
                save_button=False,
                reset_properties=False
            )
            components.html(html_content, width=1500, height=1200, scrolling=False)
else:
    st.title("请先登录！")

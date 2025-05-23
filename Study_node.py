from streamlit import session_state
import streamlit as st
import pandas as pd
from database import get_second_level_nodes, update_tree_node_properties
from utils import get_statr_study
from d3blocks import D3Blocks
from helpers import page


if page():
    d3 = D3Blocks(verbose='info', chart='tree', frame=False)

    if 'node_name' not in st.session_state:
        st.session_state.node_name = None
    if 'end' not in st.session_state:
        st.session_state.end = True

    user_id = st.session_state.get('user_info', {}).get('id', None)
    tree_name = st.session_state.tree_name

    tree_data = get_second_level_nodes(user_id, tree_name)
    if tree_data is None:
        st.warning("用户还没生成相关树，请先创建树结构。")
    else:
        df = pd.DataFrame(tree_data)
        level_1_nodes = set(df['source']) - set(df['target'])
        level_2_nodes = set(df[df['source'].isin(level_1_nodes)]['target'])

        st.title("二级节点选择框")
        selected_node = st.selectbox("请选择一个二级节点:", list(level_2_nodes))

        start_study = st.button("开始学习")
        if start_study:
            summary_placeholder = st.empty()
            summary_placeholder.markdown("")  # 清空可能残留的内容
            result = get_statr_study(tree_name, selected_node, summary_placeholder)
            st.session_state.node_name = selected_node
            st.session_state.end = False

        if st.button("完成学习", disabled=st.session_state.end):
            def update_tree_properties():
                if st.session_state.node_name is None:
                    st.error("请选择一个节点后再进行更新")
                    return

                d3.node_properties = st.session_state.tree_node_properties
                d3.node_properties.get(f'{st.session_state.node_name}')['color'] = '#000000'
                d3.node_properties.get(f'{st.session_state.node_name}')['edge_color'] = '#FF0000'
                d3.node_properties.get(f'{st.session_state.node_name}')['edge_size'] = 5

                st.session_state.tree_node_properties = d3.node_properties

                update_tree_node_properties(user_id, tree_name, st.session_state.tree_node_properties)

            update_tree_properties()
            st.success(f"节点 {st.session_state.node_name} 的属性已更新。")
else:
    st.title("请先登录！")

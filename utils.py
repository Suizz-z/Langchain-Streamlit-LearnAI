from itertools import chain
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory, SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from database import get_last_two_days_history
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import streamlit as st
from prompt import question_template, path_template, System_prompt, tree_system_prompt, user_prompt, \
    study_system_prompt, user_prompt_study

def get_llm_instance(placeholder=None):
    callbacks = [StreamlitCallbackHandler(placeholder)] if placeholder else []
    return ChatOpenAI(
        api_key="sk-d29fa2aa83b142f2aa5dc98bc3b0405b",
        model='deepseek-chat',
        base_url="https://api.deepseek.com/v1",
        streaming=True,
        callbacks=callbacks,
        verbose=True
    )


class StreamlitCallbackHandler(StreamingStdOutCallbackHandler):
    def __init__(self, summary_placeholder):
        super().__init__()
        self.summary_placeholder = summary_placeholder
        self.summary_text = ""
        self.summary_placeholder.markdown("")

    def on_llm_new_token(self, token: str, **kwargs):
        self.summary_text += token
        self.summary_placeholder.markdown(self.summary_text)


question_prompt = PromptTemplate(template=question_template,
                                 input_variables=["language", "mode", "completed_topics", "num_questions",
                                                  "question_types"])


def generate_practice_questions(language, mode, completed_topics, num_questions, question_types):
    llm = get_llm_instance()
    question_llm_chain = LLMChain(prompt=question_prompt, llm=llm)
    return question_llm_chain.run(language=language, mode=mode, completed_topics=completed_topics,
                                  num_questions=num_questions, question_types=question_types)


path_prompt = PromptTemplate(template=path_template, input_variables=["practice_questions", "user_result"])


def generate_learning_path(practice_questions, user_result, placeholder=None):
    llm = get_llm_instance(placeholder)
    path_llm_Chain = LLMChain(prompt=path_prompt, llm=llm)
    return path_llm_Chain.run(practice_questions=practice_questions, user_result=user_result)


store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
        store[session_id].add_message(AIMessage(
            content="你好！我是你的编程学习助手。我可以帮你解答编程相关的问题，或者提供编程学习的建议。请问你有什么问题吗？"))
    return store[session_id]


def get_ai_chat_stream(prompt: str, session_id: str, ai_response_placeholder):
    llm = get_llm_instance(ai_response_placeholder)
    chat_ai_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个助手"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])

    chat_chain = chat_ai_prompt | llm
    chain_with_history = RunnableWithMessageHistory(
        chat_chain,
        lambda session_id: SQLChatMessageHistory(
            session_id=session_id, connection="sqlite:///message_history.db",
        ),
        input_messages_key="question",
        history_messages_key="history",
    )
    config = {"configurable": {"session_id": session_id}}
    response = chain_with_history.invoke({"question": prompt}, config=config)
    return response.content


def summarize_learning_status_streamlit(user_id, summary_placeholder):
    history = get_last_two_days_history(user_id)
    if not history:
        summary_placeholder.write("学员在过去两天内没有答题记录。")
        return

    history_str = "\n".join([f"时间: {item[0]}, 问题: {item[1]}" for item in history])
    template = """以下是学员在过去两天的答题历史：
    {history}

    请根据以上信息，总结学员的学习状态，包括但不限于：
    - 学员的答题频率
    - 学员的答题内容难度
    - 学员的学习态度
    - 学员的进步或不足之处

    总结："""

    prompt = PromptTemplate(template=template, input_variables=["history"])
    llm_summary = get_llm_instance(summary_placeholder)  # 动态获取实例

    summarize_chain = LLMChain(llm=llm_summary, prompt=prompt)
    summarize_chain.run(history=history_str)


def get_ai_tree(language, subject):
    llm = get_llm_instance()
    prompt_tree = ChatPromptTemplate.from_messages([
        ("system", tree_system_prompt)
    ])
    tree_chain = prompt_tree | llm
    result = tree_chain.invoke({"language": language, "subject": subject})
    return result


def get_statr_study(language, node, summary_placeholder):
    llm = get_llm_instance(summary_placeholder)
    prompt_study = ChatPromptTemplate.from_messages([
        ("system", study_system_prompt),
        ("user", user_prompt_study)
    ])
    study_chain = prompt_study | llm
    result = study_chain.invoke({"language": language, "prompt_study": node})
    return result

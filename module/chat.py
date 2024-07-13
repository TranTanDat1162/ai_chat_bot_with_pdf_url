# chat.py
import joblib
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from module.fetch_pdf import load_pdf_text_chunks
from module.fetch_url import load_url_text_chunks

def get_response(query, chat_history, pdf_text_chunks, url_text_chunks):
    template = """
        You are a helpful assistant. Answer the following questions considering the history of the conversation:

        Chat history: {chat_history}

        User question: {user_question}

        PDF Text chunks: {pdf_text_chunks}

        URL Text chunks: {url_text_chunks}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI(model="gpt-4o")

    chain = prompt | llm | StrOutputParser()

    return chain.stream({
        "chat_history": chat_history,
        "user_question": query,
        "pdf_text_chunks": pdf_text_chunks,
        "url_text_chunks": url_text_chunks
    })

def load_chat_history(chat_id):
    try:
        messages = joblib.load(f'data/{chat_id}-st_messages')
        chat_history = joblib.load(f'data/{chat_id}-st_chat_history')
    except FileNotFoundError:
        messages = []
        chat_history = []
    return messages, chat_history

def save_chat_history(chat_id, messages, chat_history):
    joblib.dump(messages, f'data/{chat_id}-st_messages')
    joblib.dump(chat_history, f'data/{chat_id}-st_chat_history')

def display_chat(chat_history):
    for message in chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
        else:
            with st.chat_message("AI"):
                st.markdown(message.content)

def handle_user_input(chat_id, chat_history):
    user_query = st.chat_input("Your message:")
    if user_query:
        chat_history.append(HumanMessage(user_query))

        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            pdf_text_chunks = load_pdf_text_chunks(chat_id)
            url_text_chunks = load_url_text_chunks(chat_id)
            response = st.write_stream(get_response(user_query, chat_history, pdf_text_chunks, url_text_chunks))
            chat_history.append(AIMessage(content=response))

        return True, chat_history
    return False, chat_history

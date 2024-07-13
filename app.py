import time
import os
import joblib
import streamlit as st
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from module.chat import load_chat_history, save_chat_history, display_chat, handle_user_input
from module.fetch_pdf import handle_pdf_upload
from module.fetch_url import handle_url_upload
from sidebar import manage_sidebar  # Import hàm mới

load_dotenv()

new_chat_id = f'{time.time()}'
os.makedirs('data/', exist_ok=True)

st.set_page_config(page_title="PDFs and URLs Chat", page_icon=":robot_face:")

try:
    past_chats: dict = joblib.load('data/past_chats_list')
except FileNotFoundError:
    past_chats = {}

# Gọi hàm quản lý sidebar từ sidebar.py
manage_sidebar(past_chats, new_chat_id)

# Tạo 3 tab trong main conversation
selected_option = option_menu(
    menu_title=None,
    options=["Chat", "Import PDF", "Fetch Link"],
    icons=["chat", "file-pdf", "link"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

st.write('# Chat with PDFs and URLs :robot_face:')

if selected_option == "Chat":
    st.session_state.messages, st.session_state.chat_history = load_chat_history(st.session_state.chat_id)
    display_chat(st.session_state.chat_history)
    user_input, st.session_state.chat_history = handle_user_input(st.session_state.chat_id, st.session_state.chat_history)
    
    if user_input:
        save_chat_history(st.session_state.chat_id, st.session_state.messages, st.session_state.chat_history)
    

elif selected_option == "Import PDF":
    pdf_files = st.file_uploader("Choose a PDF file", type="pdf", accept_multiple_files=True, label_visibility="visible")
    if pdf_files and st.button("Process"):
        with st.spinner("Processing"):
            handle_pdf_upload(pdf_files, st.session_state.chat_id)
            st.success("PDF file uploaded and processed successfully!")

elif selected_option == "Fetch Link":
    urls = st.text_area("Enter URLs (one per line)").splitlines()
    if urls and st.button("Fetch"):
        with st.spinner("Fetching content"):
            handle_url_upload(urls, st.session_state.chat_id)
            st.success("URL content fetched and processed successfully!")

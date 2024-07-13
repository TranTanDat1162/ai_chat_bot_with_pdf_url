# sidebar.py
import os
import joblib
import streamlit as st

def manage_sidebar(past_chats, new_chat_id):
    with st.sidebar:
        st.subheader('Your chat history')

        if "chat_id" not in st.session_state:
            st.session_state.chat_id = st.selectbox(
                label='Pick a past chat',
                options=[new_chat_id] + list(past_chats.keys()),
                format_func=lambda x: past_chats.get(x, 'New Chat'),
                placeholder='_',
            )
        else:
            st.session_state.chat_id = st.selectbox(
                label='Pick a past chat',
                options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
                index=1,
                format_func=lambda x: past_chats.get(x, 'New Chat' if x != st.session_state.chat_id else st.session_state.get('chat_title', f'ChatSession-{x}')),
                placeholder='_',
            )

        if "chat_title" not in st.session_state:
            st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'

        new_chat_title = st.text_input("Name this conversation:", value=st.session_state.chat_title)

        if st.session_state.chat_id == new_chat_id and new_chat_title != f'ChatSession-{st.session_state.chat_id}':
            past_chats[st.session_state.chat_id] = new_chat_title
            st.session_state.chat_title = new_chat_title
            st.success("Changed successfully")
        elif new_chat_title != st.session_state.chat_title:
            st.session_state.chat_title = new_chat_title
            past_chats[st.session_state.chat_id] = new_chat_title
            joblib.dump(past_chats, 'data/past_chats_list')
            st.success("Changed successfully")

        for chat_id in list(past_chats.keys()):
            if st.button(f'Delete {past_chats[chat_id]}', key=f'delete_{chat_id}'):
                files_to_delete = [
                    f'data/{chat_id}-st_messages',
                    f'data/{chat_id}-st_chat_history',
                    f'data/{chat_id}_pdf_text_chunks.pkl',
                    f'data/{chat_id}_url_text_chunks.pkl',
                    f'data/{chat_id}.pdf'
                ]
                for file_path in files_to_delete:
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        st.warning(f"Could not delete {file_path}: {e}")
                del past_chats[chat_id]
                joblib.dump(past_chats, 'data/past_chats_list')
                if st.session_state.chat_id == chat_id:
                    del st.session_state.chat_id
                    del st.session_state.chat_title
                st.session_state.delete_success = True
                st.rerun()

        if "delete_success" in st.session_state and st.session_state.delete_success:
            st.success("Deleted chat successfully")
            del st.session_state.delete_success

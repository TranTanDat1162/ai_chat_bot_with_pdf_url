import joblib
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter

def handle_pdf_upload(pdf_files, chat_id):
    all_text = ""
    for pdf_file in pdf_files:
        pdf_path = f'data/{chat_id}.pdf'
        with open(pdf_path, "wb") as file:
            file.write(pdf_file.getvalue())
        
        pdf_reader = PyPDF2.PdfReader(pdf_path)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
        all_text += text

    text_chunks = chunk_text(all_text)
    save_text_chunks(chat_id, text_chunks)

def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_text(text)

def save_text_chunks(chat_id, text_chunks):
    joblib.dump(text_chunks, f'data/{chat_id}_pdf_text_chunks.pkl')

def load_pdf_text_chunks(chat_id):
    try:
        return joblib.load(f'data/{chat_id}_pdf_text_chunks.pkl')
    except FileNotFoundError:
        return []



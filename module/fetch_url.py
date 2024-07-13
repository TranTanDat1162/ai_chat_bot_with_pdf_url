# fetch_url.py
import requests
from bs4 import BeautifulSoup
import joblib
from langchain.text_splitter import RecursiveCharacterTextSplitter

def fetch_url_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return ""

def parse_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    return '\n'.join(chunk for chunk in chunks if chunk)

def handle_url_upload(urls, chat_id):
    all_text = ""
    for url in urls:
        html_content = fetch_url_content(url)
        text = parse_html_content(html_content)
        all_text += text + "\n\n"

    text_chunks = chunk_text(all_text)
    save_text_chunks(chat_id, text_chunks)

def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_text(text)

def save_text_chunks(chat_id, text_chunks):
    joblib.dump(text_chunks, f'data/{chat_id}_url_text_chunks.pkl')

def load_url_text_chunks(chat_id):
    try:
        return joblib.load(f'data/{chat_id}_url_text_chunks.pkl')
    except FileNotFoundError:
        return []

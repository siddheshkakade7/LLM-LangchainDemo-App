# Loads and splits the document into chunks

import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import Config

def load_documents():
    path = os.path.join(Config.DATA_DIR, Config.DATA_FILE)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    return [Document(page_content=text)]

def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    return splitter.split_documents(docs)

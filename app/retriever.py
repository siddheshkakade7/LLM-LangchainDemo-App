# Builds FAISS vector store and returns retriever

from langchain_community.vectorstores import FAISS
from app.loader import load_documents, split_documents
from app.embedder import get_embeddings

_vectorstore = None

def build_vectorstore():
    global _vectorstore
    if _vectorstore:
        return _vectorstore
    docs = load_documents()
    chunks = split_documents(docs)
    embeddings = get_embeddings()
    _vectorstore = FAISS.from_documents(chunks, embeddings)
    return _vectorstore

def get_retriever(k=4):
    vs = build_vectorstore()
    return vs.as_retriever(search_kwargs={"k": k})

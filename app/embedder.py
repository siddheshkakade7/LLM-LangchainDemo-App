# Creates embedding model for vectorization

from langchain_openai import OpenAIEmbeddings
from app.config import Config

def get_embeddings():
    return OpenAIEmbeddings(
        api_key=Config.OPENAI_API_KEY,
        model=Config.EMBEDDINGS_MODEL
    )

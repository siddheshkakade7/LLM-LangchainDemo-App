# Loads environment variables and validates required fields

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
    EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "text-embedding-3-small")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
    DATA_DIR = os.getenv("DATA_DIR", "data")
    DATA_FILE = os.getenv("DATA_FILE", "sample.txt")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))

    @classmethod
    def validate(cls):
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY missing in .env")

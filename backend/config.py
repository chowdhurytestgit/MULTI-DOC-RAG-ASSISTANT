from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()


# Project paths
UPLOAD_FOLDER = "../data/uploads"
FAISS_PATH = "../data/faiss_index"


# Embedding model (local)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
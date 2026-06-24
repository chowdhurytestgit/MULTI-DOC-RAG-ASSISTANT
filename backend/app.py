from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware

import os
import shutil

from config import UPLOAD_FOLDER


from document_loader import (
    load_documents,
    split_documents
)


from vector_store import (
    create_vector_store,
    save_vector_store
)


from rag_pipeline import RAGPipeline


from models import (
    ChatRequest,
    ChatResponse,
    ClearChatRequest,
    MessageResponse
)


# ------------------------------
# FastAPI App
# ------------------------------

app = FastAPI(
    title="Multi Document RAG Assistant",
    version="1.0"
)


# ------------------------------
# CORS
# ------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ------------------------------
# Initialize RAG
# ------------------------------

rag = RAGPipeline()


# ------------------------------
# Home
# ------------------------------

@app.get("/")
def home():
    return {
        "message": "RAG API Running"
    }


# ------------------------------
# Upload Documents
# ------------------------------

@app.post(
    "/upload",
    response_model=MessageResponse
)
async def upload_file(
    file: UploadFile = File(...)
):
    global rag

    try:
        # Create upload directory
        os.makedirs(
            UPLOAD_FOLDER,
            exist_ok=True
        )

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        # Load all documents
        documents = load_documents(
            UPLOAD_FOLDER
        )


        # Create chunks
        chunks = split_documents(
            documents
        )


        # Create FAISS database
        vector_db = create_vector_store(
            chunks
        )


        # Save updated index
        save_vector_store(
            vector_db
        )


        # IMPORTANT:
        # Reload RAG with new FAISS index
        rag = RAGPipeline()


        return {
            "message":
            f"{file.filename} uploaded successfully and chatbot updated."
        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ------------------------------
# Chat Endpoint
# ------------------------------

@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest
):

    try:

        result = rag.ask(
            request.question,
            request.session_id
        )


        return result


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ------------------------------
# Clear Chat
# ------------------------------

@app.post(
    "/clear-chat",
    response_model=MessageResponse
)
def clear_chat(
    request: ClearChatRequest
):

    try:

        rag.clear_chat(
            request.session_id
        )


        return {
            "message":
            "Chat history cleared successfully."
        }


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
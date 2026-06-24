from pydantic import BaseModel
from typing import List


# -----------------------------
# Chat Request
# -----------------------------

class ChatRequest(BaseModel):
    question: str
    session_id: str


# -----------------------------
# Chat Response
# -----------------------------

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]


# -----------------------------
# Clear Chat Request
# -----------------------------

class ClearChatRequest(BaseModel):
    session_id: str


# -----------------------------
# API Message Response
# -----------------------------

class MessageResponse(BaseModel):
    message: str
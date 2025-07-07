from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    title:str
    long_answer: str

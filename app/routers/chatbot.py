"""Chatbot router: Simple generative AI using LangChain for text-to-response."""

import os
import json
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from langchain_groq import ChatGroq
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"],
    responses={404: {"description": "Not found"}}
)

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

llm = ChatGroq(
    model="gemma2-9b-it",
    api_key=os.getenv("GROQ_API_KEY"))

with open("app/memory/chat-history.json") as f:
    data = json.load(f)

# simple chatbot with message history
@router.post("/ask", response_model=ChatResponse, summary="Ask chatbot a question")
async def ask_question(request: ChatRequest):
    """
    Ask a question to the generative AI chatbot.
    """
    try:
        messages = list(map(lambda x: HumanMessage(content=x["content"]) if x["role"] == "human" else AIMessage(content=x["content"]), data["data"]))
        prompt_history = ChatPromptTemplate.from_messages(
            
            [
                *messages,
                MessagesPlaceholder(variable_name="question"),
            ]
        )
        
        formatted_prompt = prompt_history.invoke({"question": [HumanMessage(content=request.question)]})
        answer = llm.invoke(formatted_prompt)
        response = ChatResponse(answer=answer.content)

        with open("app/memory/chat-history.json", "w") as f:
            data["data"].append({"role": "human", "content": request.question})
            data["data"].append({"role": "ai", "content": answer.content})
            json.dump(data, f)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

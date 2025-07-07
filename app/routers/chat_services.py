from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import asc, desc, select
from app.config.db_config import get_session
from app.model.chat_content import ChatContent
from app.model.chat_session import ChatSession
from app.schemas.chat_schema import ChatRequest, ChatResponse
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from app.config.llm_config import llm
from sqlalchemy.orm import selectinload

router=APIRouter(
    prefix="/chat",
    tags=["chat"],
)

@router.post("/start-chat", response_model=ChatResponse, summary="Start new AI chat session")
async def start_chat(request: ChatRequest, db: AsyncSession = Depends(get_session)):
    try:
        formatted_prompt: ChatResponse = llm.with_structured_output(ChatResponse).invoke(request.question)
        session_obj: ChatSession = ChatSession(title=formatted_prompt.title)
        db.add(session_obj)
        
        await db.flush()  # Ensure session_obj.id is populated
        
        db.add_all([
            ChatContent(chat_session_id=session_obj.id, content=request.question, role="human"),
            ChatContent(chat_session_id=session_obj.id, content=formatted_prompt.long_answer, role="ai")
        ])
        
        await db.commit()
        db.close()
        
        return formatted_prompt
    except Exception as e:
        db.rollback()
        db.close()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/start-chat/{id}", response_model=ChatResponse, summary="Continue AI chat session")
async def continue_chat(request: ChatRequest, id: str, db: AsyncSession = Depends(get_session)):
    try:
        query = select(ChatContent).where(ChatContent.chat_session_id == id).order_by(desc(ChatContent.created_at))
        messages = list(map(lambda x: HumanMessage(content=x.content) if x.role == "human" else AIMessage(content=x.content), await db.scalars(query)))
        prompt_history=ChatPromptTemplate.from_messages([
            *messages,
            MessagesPlaceholder(variable_name="question"),
        ])
        formatted_prompt= prompt_history.invoke({"question": [HumanMessage(content=request.question)]})
        answer:ChatResponse=llm.with_structured_output(ChatResponse).invoke(formatted_prompt)
        
        db.add_all([
            ChatContent(chat_session_id=id, content=request.question, role="human"),
            ChatContent(chat_session_id=id, content=answer.long_answer, role="ai")
        ])
        
        await db.commit()
        db.close()
        
        return answer
    except Exception as e:
        db.rollback()
        db.close()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat-session", response_model=list[ChatSession], summary="Get all chat session")
async def get_chat_session(db: AsyncSession = Depends(get_session)):
    try:
        return await db.scalars(select(ChatSession))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/chat-session/{id}", response_model=ChatSession, summary='Get chat session by ID')
async def get_chat_session_by_id(id, db:AsyncSession=Depends(get_session)):
    try:
        query = select(ChatSession).where(ChatSession.id==id).options(selectinload(ChatSession.chat_content))
        result= await db.execute(query)
        return result.scalar_one_or_none()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat-history/{id}", response_model=list[ChatContent], summary="Get chat history based on session ID")
async def get_chat_history(id: str, db: AsyncSession = Depends(get_session)):
    try:
        query = select(ChatContent).where(ChatContent.chat_session_id == id).order_by(asc(ChatContent.created_at))
        return await db.scalars(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))        


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import asc, desc, select
from app.config.db_config import get_session
from app.model.chat_content import ChatContent
from app.model.chat_session import ChatSession
from app.schemas.chat_content_schema import ChatContentSchema
from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatSummary
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from app.config.llm_config import llm
from app.config.sbert_config import sbert_model
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
            ChatContent(chat_session_id=session_obj.id, content=request.question, role="human", embedding=sbert_model.encode(request.question)),
            ChatContent(chat_session_id=session_obj.id, content=formatted_prompt.long_answer, role="ai", embedding=sbert_model.encode(formatted_prompt.long_answer))
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
        new_query = text("""
            select * from chat_content c
            where c.chat_session_id= :chat_session_id
            ORDER BY c.embedding <#> :embedding_vector
            LIMIT 5""")

        result=await db.execute(new_query, {
            "chat_session_id":id,
            "embedding_vector": f"[{', '.join(map(str, sbert_model.encode(request.question).tolist()))}]" 
        })
        
        
        result_data:list[ChatContent] = result.all()

        messages = list(map(lambda x: HumanMessage(content=x.content) if x.role == "human" else AIMessage(content=x.content), result_data))

        prompt_history=ChatPromptTemplate.from_messages([
            *messages,
            MessagesPlaceholder(variable_name="question"),
        ])
        formatted_prompt= prompt_history.invoke({"question": [HumanMessage(content=request.question)]})
        answer:ChatResponse=llm.with_structured_output(ChatResponse).invoke(formatted_prompt)
        
        db.add_all([
            ChatContent(chat_session_id=id, content=request.question, role="human", embedding=sbert_model.encode(request.question)),
            ChatContent(chat_session_id=id, content=answer.long_answer, role="ai", embedding=sbert_model.encode(answer.long_answer))
        ])
        
        await db.commit()
        db.close()
        
        return answer
    except Exception as e:
        db.rollback()
        db.close()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/chat-summary/{id}", response_model=ChatSummary, summary="Summarize prompt")
async def summarize_chat(id: str, db: AsyncSession = Depends(get_session)):
    try:
        query = select(ChatContent).where(ChatContent.chat_session_id == id).order_by(desc(ChatContent.created_at))
        messages = list(map(lambda x: HumanMessage(content=x.content) if x.role == "human" else AIMessage(content=x.content), await db.scalars(query)))
        prompt_history=ChatPromptTemplate.from_messages([
            *messages,
            MessagesPlaceholder(variable_name="question"),
            
        ])
        answer:ChatSummary=llm.with_structured_output(ChatSummary).invoke(prompt_history.invoke({"question": [HumanMessage(content='Please summarize above prompts')]}))
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
    5
@router.get("/chat-session/{id}", response_model=ChatSession, summary='Get chat session by ID')
async def get_chat_session_by_id(id, db:AsyncSession=Depends(get_session)):
    try:
        query = select(ChatSession).where(ChatSession.id==id).options(selectinload(ChatSession.chat_content))
        result= await db.execute(query)
        return result.scalar_one_or_none()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat-history/{id}", response_model=list[ChatContentSchema], summary="Get chat history based on session ID")
async def get_chat_history(id: str, db: AsyncSession = Depends(get_session)):
    try:
        query = select(ChatContent).where(ChatContent.chat_session_id == id).order_by(asc(ChatContent.created_at))
        return await db.scalars(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))        


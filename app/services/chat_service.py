from fastapi import HTTPException
from app.schemas.chat_schema import ChatAgentic, ChatRequest, ChatResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union
from app.config.llm_config import llm
from app.model.chat_session import ChatSession
from app.model.chat_content import ChatContent
from app.config.sbert_config import sbert_model
from app.schemas.ticket_trans_schema import TicketAgenticChatSch

async def start_new_chat(request:ChatRequest, db:AsyncSession, response:Union[ChatResponse, ChatAgentic, TicketAgenticChatSch]):
    try:
        formatted_prompt:Union[ChatResponse, ChatAgentic, TicketAgenticChatSch] = llm.with_structured_output(response).invoke(request.question)
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
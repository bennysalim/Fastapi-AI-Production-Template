from fastapi import APIRouter, Depends, HTTPException

from app.schemas.ticket_trans_schema import TicketAgenticChatSch
from app.schemas.chat_schema import ChatRequest
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.db_config import get_session
from app.services.chat_service import start_new_chat
from app.workflow.ticket_trans_graph import ticket_trans_workflow


router=APIRouter(
    prefix="/ticket-agentic",
    tags=["ticket-agentic"],
)

@router.post("/start-chat", response_model=TicketAgenticChatSch, summary="Ticket Agentic AI Chat")
async def start_ticket_agentic_chat(request:ChatRequest, db: AsyncSession = Depends(get_session)):
    # inference basic ai chat
    response:TicketAgenticChatSch = await start_new_chat(request, db, TicketAgenticChatSch)
    # pemanfaatan agent
    result = ticket_trans_workflow.invoke(response)
    return result
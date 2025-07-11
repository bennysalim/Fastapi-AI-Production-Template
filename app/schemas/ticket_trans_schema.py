from typing import Optional
from pydantic import BaseModel

from app.enums.agent_inference_enum.ticket_inference_enum import TicketInferenceEnum
from app.enums.ticket_status_enum import TicketStatusEnum
from app.enums.ticket_type_enum import TicketTypeEnum
from app.schemas.chat_schema import ChatAgentic

class TicketTransSch(BaseModel):
    project_code:Optional[str]
    unit_code:Optional[str]
    ticket_summary:str
    ticket:TicketStatusEnum
    type:TicketTypeEnum

class TicketAgenticChatSch(TicketTransSch, ChatAgentic):
    ticket_agent_inference:TicketInferenceEnum
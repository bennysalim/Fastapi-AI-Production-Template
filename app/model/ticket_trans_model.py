from pydantic import BaseModel

from app.enums.agent_inference_enum import AgentInferenceEnum
from app.enums.ticket_status_enum import TicketStatusEnum
from app.enums.ticket_type_enum import TicketTypeEnum


class TicketTransModel(BaseModel):
    prompt_answer:str
    project:str
    unit:str
    ticket_summary:str
    ticket:TicketStatusEnum
    type:TicketTypeEnum
    agent_inference:AgentInferenceEnum
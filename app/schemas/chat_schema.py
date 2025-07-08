from pydantic import BaseModel

from app.enums.agent_inference_enum import AgentInferenceEnum
from app.model.ticket_trans_model import TicketTransModel


class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    title:str
    long_answer: str
    agent_inference:AgentInferenceEnum
    expected_agent_schema:TicketTransModel
    flutter_agent_schema_field_validator:list[str]

class ChatSummary(BaseModel):
    very_long_summary:str
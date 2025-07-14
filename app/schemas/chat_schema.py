from pydantic import BaseModel

from app.schemas.field_validator_schema import FieldValidatorSchema

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    title:str
    long_answer: str

class ChatSummary(BaseModel):
    very_long_summary:str

class ChatAgentic(ChatResponse):
    invalid_schema_field:list['FieldValidatorSchema']
    is_schema_valid:bool
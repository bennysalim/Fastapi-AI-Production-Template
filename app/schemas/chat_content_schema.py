import datetime
from typing import Optional

from app.model.base_model import BaseModel


class ChatContentSchema(BaseModel):
    id: str
    chat_session_id: str
    content: str
    role: str
    # Note: embedding field is excluded
    
    class Config:
        from_attributes = True

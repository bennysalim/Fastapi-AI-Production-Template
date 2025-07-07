from sqlmodel import Field, Relationship, SQLModel

from app.model.base_model import BaseULIDModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.model.chat_content import ChatContent

class ChatSessionBase(SQLModel):
    title: str = Field(nullable=True, default=None)

class ChatSessionFullBase(ChatSessionBase, BaseULIDModel):
    pass

class ChatSession(ChatSessionFullBase, table=True):
    __tablename__ = "chat_session"
    chat_content: list["ChatContent"] = Relationship(back_populates="chat_session", 
                                                     sa_relationship_kwargs={'lazy': 'select'})
    
    class Config:
        from_attributes=True

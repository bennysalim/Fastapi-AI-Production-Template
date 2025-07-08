from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel
from app.model.base_model import BaseModel
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from app.model.chat_session import ChatSession

class ChatContentBase(SQLModel):
    chat_session_id:str = Field(nullable=False, foreign_key="chat_session.id")
    content:str = Field(nullable=False)
    embedding: Optional[list[float]] = Field(
        default=None,
        sa_column=Column(Vector(384), nullable=True)
    )
    role:str = Field(nullable=False)

    class Config:
        arbitrary_types_allowed = True
        from_attributes=True

class ChatContentFullBase(ChatContentBase, BaseModel):
    pass

class ChatContent(ChatContentFullBase, table=True):
    __tablename__="chat_content"
    chat_session:'ChatSession' = Relationship(back_populates="chat_content", sa_relationship_kwargs={'lazy': 'select'})
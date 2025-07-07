from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel
from pgvector.sqlalchemy import Vector
from app.model.base_model import BaseModel, BaseULIDModel

from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from app.model.chat_session import ChatSession

class ChatContentBase(SQLModel):
    chat_session_id:str = Field(nullable=False, foreign_key="chat_session.id")
    content:str = Field(nullable=False)
    # embedding: Annotated[list[float], Field(sa_column=Column(Vector(1536)))]
    role:str = Field(nullable=False)

    class Config:
        arbitrary_types_allowed = True
        from_attributes=True

class ChatContentFullBase(ChatContentBase, BaseModel):
    pass

class ChatContent(ChatContentFullBase, table=True):
    __tablename__="chat_content"
    chat_session:'ChatSession' = Relationship(back_populates="chat_content", sa_relationship_kwargs={'lazy': 'select'})
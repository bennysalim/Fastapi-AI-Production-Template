from pydantic import BaseModel

from app.schemas.chat_content_schema import ChatContentSchema


class ChatSessionSchema(BaseModel):
    id:str
    title:str
    chat_content:list["ChatContentSchema"]

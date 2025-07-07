from fastapi import APIRouter, Depends, HTTPException
from app.model.chat_content import ChatContent
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.db_config import get_session
from sqlmodel import asc, select

router=APIRouter(
    prefix="/chat-content",
    tags=["chat-content"],
    responses={404: {"description": "Not found"}}
)


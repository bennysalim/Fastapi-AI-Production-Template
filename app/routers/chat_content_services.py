from fastapi import APIRouter

router=APIRouter(
    prefix="/chat-content",
    tags=["chat-content"],
    responses={404: {"description": "Not found"}}
)


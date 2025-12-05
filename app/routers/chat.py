from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.ai_core.service import process_chat_message

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str

@router.post("/message")
async def chat_message(request: ChatRequest):
    try:
        response = await process_chat_message(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

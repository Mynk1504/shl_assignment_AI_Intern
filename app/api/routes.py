from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.services.agent import AgentService
from app.api.dependencies import get_agent_service
from app.core.logger import logger

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest, 
    agent_service: AgentService = Depends(get_agent_service)
):
    """
    Accepts conversation history and returns the SHL Assessment Agent's next response.
    """
    try:
        response = agent_service.generate_response(request)
        return response
    except Exception as e:
        logger.error(f"Failed to generate response: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while processing chat.")

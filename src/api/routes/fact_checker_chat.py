from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi import Request
from services import fact_checker_chat
from ..schemas.factual_answering_chat import FactualCheckerChatRequest

router = APIRouter(prefix="/factual-answering-chat")

@router.post('/')
async def chat(body: FactualCheckerChatRequest, request: Request):
    llm_client = request.app.state.llm_client
    return StreamingResponse(fact_checker_chat.start_fact_checker_chat(body.prompt, llm_client))


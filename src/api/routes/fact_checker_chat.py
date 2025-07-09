from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse

from src.services import refact
from src.services.refact import (
    RefactGeneric,
    RefactException,
    ActException,
    ReasonException,
    ZeroDivisionCustomException,
)

from ..schemas.refact import (
    ActRequest,
    RefactRequest,
    ReasonRequest,
    ReasonResponse,
    ActResponse,
)

router = APIRouter(prefix="/v1")


@router.post("/refact")
async def refact_chat(body: RefactRequest, request: Request):
    llm_client = request.app.state.llm_client
    try:
        return StreamingResponse(refact.refact(body.prompt, llm_client))
    except (
        RefactGeneric,
        RefactException,
        ActException,
        ReasonException,
        ZeroDivisionCustomException,
    ) as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/act", response_model=ActResponse)
async def act_chat(body: ActRequest, request: Request):
    try:
        return {"result": await refact.act(body.action)}
    except (
        RefactGeneric,
        RefactException,
        ActException,
        ReasonException,
        ZeroDivisionCustomException,
    ) as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reason", response_model=ReasonResponse)
async def reason_chat(body: ReasonRequest, request: Request):
    llm_client = request.app.state.llm_client
    try:
        return {"text": await refact.reason(body.prompt, llm_client)}
    except (
        RefactGeneric,
        RefactException,
        ActException,
        ReasonException,
        ZeroDivisionCustomException,
    ) as e:
        raise HTTPException(status_code=500, detail=str(e))

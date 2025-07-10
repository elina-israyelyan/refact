from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from api.routes.fact_checker_chat import router as refact_router
from llm import ClientFactory
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app.state.llm_client = ClientFactory.get_client(settings.LLM_CLIENT_TYPE)
    yield


app = FastAPI(docs_url="/docs", redoc_url="/redoc", lifespan=lifespan)

app.include_router(refact_router)

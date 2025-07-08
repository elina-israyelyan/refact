from fastapi import FastAPI
from contextlib import asynccontextmanager
from llm import ClientFactory
from api.routes.fact_checker_chat import router as refact_router
from settings import settings
@asynccontextmanager
async def lifespan(app):
    app.state.llm_client = await ClientFactory.get_client(settings.LLM_CLIENT_TYPE) 
    yield

app = FastAPI(docs_url="/docs", redoc_url="/redoc", lifespan=lifespan)

app.include_router(refact_router)

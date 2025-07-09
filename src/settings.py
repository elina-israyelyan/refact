from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LLM_CLIENT_TYPE: str = "gemini"  # Options: 'gemini', 'mock'
    GEMINI_SA_CREDENTIAL_PATH: str
    WIKI_CLIENT_TYPE: str = "real"  # Options: 'real', 'mock'


settings = Settings()

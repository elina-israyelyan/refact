from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LLM_CLIENT_TYPE: str = "gemini"  # Options: 'gemini', 'mock'
    WIKI_CLIENT_TYPE: str = "real"   # Options: 'real', 'mock'
    # Add other base/global settings here as needed

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

settings = Settings() 
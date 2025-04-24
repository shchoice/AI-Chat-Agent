import os
from functools import lru_cache

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    # OpenAI 설정
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL_NAME: str = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
    OPENAI_TEMPERATURE: int = os.getenv("OPENAI_TEMPERATURE", 0.01)

    # 서버 설정
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "RAG API"
    DEBUG: bool = False

    # 임베딩 모델
    EMBEDDING_MODEL_NAME: str = "BAAI/bge-m3"

    # 벡터 저장소 설정
    FAISS_EMBEDDING_DIMENSION: int = 1024

    # LLAMA Index 설정
    LLAMA_CLOUD_API_KEY: str = os.getenv("LLAMA_CLOUD_API_KEY", "llx-default-llama-key")
    LLAMA_INDEX_LLM_MODEL: str = os.getenv("LLAMA_INDEX_LLM_MODEL", "openai-gpt4o")
    LLAMA_PDF_PARSER_RESULT_TYPE: str = "markdown"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()

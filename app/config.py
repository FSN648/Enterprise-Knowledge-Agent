from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    vector_backend: str = "chroma"
    pinecone_api_key: str = ""
    pinecone_index: str = "enterprise-assistant"
    pinecone_namespace: str = "default"

    chroma_dir: str = "./data/chroma"
    documents_dir: str = "./data/documents"

    mcp_server_url: str = "http://localhost:8001/mcp"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

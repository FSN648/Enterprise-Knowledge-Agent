from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    session_id: str | None = None


class Source(BaseModel):
    content: str
    source: str
    page: int | None = None
    score: float | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source] = []


class IngestResponse(BaseModel):
    documents: int
    chunks: int

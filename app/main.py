from fastapi import FastAPI, HTTPException

from .agent import chat
from .rag import ingest_documents
from .schemas import ChatRequest, ChatResponse, IngestResponse, Source

app = FastAPI(
    title="Agentic Enterprise Knowledge Assistant",
    version="1.0.0",
    description="LLM + LangGraph + RAG + MCP portfolio project",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest", response_model=IngestResponse)
def ingest():
    try:
        docs, chunks = ingest_documents()
        return IngestResponse(documents=docs, chunks=chunks)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        answer, raw_sources = chat(request.message)
        sources = [
            Source(
                content=item["content"][:500],
                source=item["source"],
                page=item.get("page"),
                score=item.get("score"),
            )
            for item in raw_sources
        ]
        return ChatResponse(answer=answer, sources=sources)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

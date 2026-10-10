# Agentic Enterprise Knowledge Assistant

A production-oriented portfolio project demonstrating:

- LLM application development
- Prompt engineering
- RAG with semantic retrieval
- Pinecone integration with a local Chroma fallback
- LangChain + LangGraph agent orchestration
- MCP server exposing reusable enterprise tools
- FastAPI REST API
- document ingestion for PDF/TXT/MD/DOCX
- source citations
- Docker
- evaluation-ready architecture

## Architecture

```text
                    ┌─────────────────────┐
                    │  Client / Web App   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │   /chat /ingest     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     LangGraph       │
                    │  Agent + Tool Node   │
                    └───────┬─────┬───────┘
                            │     │
                ┌───────────┘     └─────────────┐
                ▼                               ▼
        ┌──────────────┐                 ┌──────────────┐
        │ RAG Search   │                 │ MCP Tools    │
        │ Pinecone /   │                 │ policies /   │
        │ Chroma       │                 │ documents    │
        └──────┬───────┘                 └──────────────┘
               │
               ▼
        ┌──────────────┐
        │ OpenAI LLM   │
        └──────────────┘
```

## Quick start

### 1. Create environment

```bash
cp .env.example .env
```

At minimum set:

```env
OPENAI_API_KEY=...
```

For Pinecone:

```env
VECTOR_BACKEND=pinecone
PINECONE_API_KEY=...
PINECONE_INDEX=enterprise-assistant
```

If Pinecone is not configured, use:

```env
VECTOR_BACKEND=chroma
```

### 2. Install

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Ingest sample documents

```bash
python -m app.ingest
```

### 4. Run API

```bash
uvicorn app.main:app --reload --port 8000
```

Open:

```text
http://localhost:8000/docs
```

### 5. Run / inspect the MCP server

The project includes a real MCP server in `mcp_server/server.py`.

For local development and inspection, use the MCP SDK CLI:

```bash
mcp dev mcp_server/server.py
```

This opens the MCP Inspector and lets you discover/call:

- `search_company_knowledge`
- `get_company_policy`
- `list_company_documents`

For a deployed Streamable HTTP setup, use the transport entry point supported by your installed MCP SDK version; the official MCP Python SDK currently documents Streamable HTTP as a supported transport.

The MCP server exposes:

- `search_company_knowledge`
- `get_company_policy`
- `list_company_documents`

## Example request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What is our annual leave policy?"}'
```

## What makes this portfolio project stronger than a basic RAG chatbot

1. Agent decides when retrieval is needed.
2. Retrieval results contain source metadata.
3. LLM is instructed to avoid unsupported claims.
4. MCP tools are exposed as a separate standard tool server.
5. Vector backend is abstracted behind a repository.
6. API layer is independent from the agent.
7. Ingestion is a separate pipeline.
8. The codebase is Docker-ready and testable.

## Suggested demo questions

- What is the annual leave policy?
- What is the remote work policy?
- What is the expense reimbursement limit?
- What information do we have about onboarding?
- If the documents do not contain the answer, say that you do not have enough evidence.

## Production extensions

- PostgreSQL for conversation state
- Redis for caching
- reranking model
- hybrid BM25 + vector retrieval
- LangSmith tracing
- authentication / RBAC
- background ingestion jobs
- evaluation dataset and RAG metrics
- streaming responses
- frontend in Next.js

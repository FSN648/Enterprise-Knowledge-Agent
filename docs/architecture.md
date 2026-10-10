# Architecture Notes

## Agent loop

```text
START
  |
  v
LLM Agent
  |
  +---- no tool call ----> END
  |
  +---- tool call --------> ToolNode
                              |
                              v
                           LLM Agent
```

The agent is intentionally simple enough to understand in an interview.

## RAG boundary

The `app/rag.py` module hides the vector database implementation.
The rest of the application calls:

```python
search(query)
```

This allows Pinecone to be replaced by Chroma during local development.

## Security improvements for production

- JWT/OAuth authentication
- tenant isolation
- document-level ACL metadata
- prompt injection defenses
- PII redaction
- rate limiting
- audit logs
- secret management

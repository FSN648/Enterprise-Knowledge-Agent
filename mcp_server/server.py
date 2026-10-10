from pathlib import Path
from mcp.server.fastmcp import FastMCP

from app.config import get_settings
from app.rag import search

settings = get_settings()

mcp = FastMCP(
    "Enterprise Knowledge Tools",
    instructions="Reusable tools for enterprise knowledge retrieval.",
)


@mcp.tool()
def search_company_knowledge(query: str, limit: int = 5) -> list[dict]:
    """Search company documents using semantic retrieval."""
    return search(query, k=limit)


@mcp.tool()
def get_company_policy(policy_name: str) -> dict:
    """Retrieve evidence for a named company policy."""
    results = search(policy_name, k=5)
    return {
        "policy": policy_name,
        "results": results,
    }


@mcp.tool()
def list_company_documents() -> list[str]:
    """List documents currently available to the ingestion pipeline."""
    root = Path(settings.documents_dir)
    root.mkdir(parents=True, exist_ok=True)
    return [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()]


# For MCP SDK versions supporting FastMCP's streamable HTTP transport.
# If your installed SDK exposes a different ASGI helper, run:
#     mcp dev mcp_server/server.py
# and use the generated Inspector workflow.
if __name__ == "__main__":
    mcp.run(transport="streamable-http")

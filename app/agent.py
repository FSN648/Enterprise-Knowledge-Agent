from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from .config import get_settings
from .rag import search

settings = get_settings()


SYSTEM_PROMPT = """You are an enterprise knowledge assistant.

Rules:
1. Use the knowledge_search tool when the user asks about company-specific information.
2. Do not invent company policies or facts.
3. Ground company-specific claims in retrieved evidence.
4. If the evidence is insufficient, explicitly say that you do not have enough evidence.
5. Cite sources in the final answer using [Source: filename, page N] when page information exists.
6. Be concise but useful.
"""


@tool
def knowledge_search(query: str) -> str:
    """Search the enterprise knowledge base using semantic vector retrieval."""
    results = search(query, k=5)

    if not results:
        return "No relevant documents were found."

    blocks = []
    for i, item in enumerate(results, start=1):
        page = item.get("page")
        location = f", page {page}" if page else ""
        blocks.append(
            f"[RESULT {i}] Source: {item['source']}{location}\n"
            f"{item['content']}"
        )

    return "\n\n".join(blocks)


TOOLS = [knowledge_search]


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def build_agent():
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    llm = ChatOpenAI(
        model=settings.openai_model,
        temperature=0,
        api_key=settings.openai_api_key,
    ).bind_tools(TOOLS)

    def call_model(state: AgentState):
        messages = [SystemMessage(content=SYSTEM_PROMPT), *state["messages"]]
        return {"messages": [llm.invoke(messages)]}

    graph = StateGraph(AgentState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", ToolNode(TOOLS))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges(
        "agent",
        tools_condition,
        {"tools": "tools", END: END},
    )
    graph.add_edge("tools", "agent")

    return graph.compile()


def chat(message: str) -> tuple[str, list[dict]]:
    agent = build_agent()
    result = agent.invoke({"messages": [HumanMessage(content=message)]})

    answer = result["messages"][-1].content

    # Re-run retrieval only for citation extraction. In production this can be
    # carried through graph state to avoid the second query.
    sources = []
    if any(word in message.lower() for word in ["policy", "company", "leave", "remote", "expense", "onboarding"]):
        try:
            sources = search(message, k=5)
        except Exception:
            sources = []

    return answer, sources

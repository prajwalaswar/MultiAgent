from typing import List
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from ..core.config import get_settings


def run_agent(provider: str, model_name: str, messages: List[str], allow_search: bool, system_prompt: str) -> str:
    settings = get_settings()

    # Keep it simple: pass api_key directly from Settings (loaded from .env)
    if provider == "Groq":
        llm = ChatGroq(model=model_name, api_key=settings.groq_api_key)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model=model_name, api_key=settings.openai_api_key)
    else:
        raise ValueError("Unsupported provider")

    # Pass Tavily key explicitly when search is enabled
    tools = []
    if allow_search:
        tools = [TavilySearchResults(max_results=2, tavily_api_key=settings.tavily_api_key)]

    # Convert raw strings to LangChain messages
    lc_messages = []
    if system_prompt:
        lc_messages.append(SystemMessage(content=system_prompt))
    for msg in messages:
        if msg and msg.strip():
            lc_messages.append(HumanMessage(content=msg))

    agent = create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=system_prompt or "",
    )

    state = {"messages": lc_messages}
    response = agent.invoke(state)
    ai_messages = [m.content for m in response.get("messages") if isinstance(m, AIMessage)]
    return ai_messages[-1] if ai_messages else ""

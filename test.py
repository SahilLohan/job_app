from langchain_ollama import ChatOllama
from langchain_core.tools import tool


@tool
def search_company_careers(company: str) -> str:
    """
    Search the web for the official careers page of a company.
    """
    return f"Searching careers page for {company}"


llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


agent_llm = llm.bind_tools(
    [search_company_careers]
)


response = agent_llm.invoke(
    """
Find the official careers page for TCS.
Use the available tools.
"""
)


print("=" * 60)
print("CONTENT")
print("=" * 60)

print(response.content)


print()
print("=" * 60)
print("TOOL CALLS")
print("=" * 60)

print(response.tool_calls)
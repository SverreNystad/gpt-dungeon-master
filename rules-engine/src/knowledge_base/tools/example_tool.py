from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

@tool
def example_tool():
    """Example tool. Returns 2 + 2"""
    return 2 + 2


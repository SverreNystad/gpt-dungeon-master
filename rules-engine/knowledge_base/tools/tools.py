from tools.example_tool import example_tool
from langchain_core.tools import StructuredTool

def get_tools() -> list[StructuredTool]:
    tools = []
    tools.append(example_tool)
    return tools

import os
from config import OPENAI_API_KEY
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from models.models import OpenAIModels 
from tools.tools import get_tools


class Agent():
    """
    A class that specifies which LLM-model to use and if it has access to tools
    """
    model = ChatOpenAI(
            model = OpenAIModels.gpt_4o_mini,
            temperature=0,
            max_tokens=16384, # Max tokens for mini. For gpt4o it's 128k
        )
    model = model.bind_tools(get_tools())

    
    
    

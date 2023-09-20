from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.agents import initialize_agent
import logging
from src.npc_generation import generate_npc

# Set up logging
logger = logging.getLogger(__name__)

def dummy_func():
    return "dummy"

tools = [
    Tool(
        name = "NPC Generator",
        func=generate_npc(),
        description="Generates a NPC based on the given prompt."
    ),
]



memory = ConversationBufferMemory(memory_key="chat_history")

llm=OpenAI(temperature=0)
agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)


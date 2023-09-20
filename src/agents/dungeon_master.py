from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.agents import initialize_agent
import logging
from src.npc_generation import generate_npc
from src.text_generation.text_generator import get_default_text_generator

# Set up logging
logger = logging.getLogger(__name__)

tools = [
    Tool(
        name = "NPC Generator",
        func=generate_npc(),
        description="Generates a NPC based on the given prompt."
    ),
]



memory = ConversationBufferMemory(memory_key="chat_history")

llm = get_default_text_generator(temperature=0.7, is_llm=False)

agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)


from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
import logging
from src.npc_generation import generate_npc
from src.referee import decide_difficulty
from src.text_generation.text_generator import get_default_text_generator

# Set up logging
logger = logging.getLogger(__name__)

tools = [
    Tool(
        name = "NPC Generator",
        func=generate_npc(),
        description="Generates a NPC based on the given prompt."
    ),
    Tool(
        name = "Difficulty Analyzer",
        func=decide_difficulty(),
        description="Decides the difficulty of the challenge based on the context."
    ),
]



memory = ConversationBufferMemory(memory_key="chat_history")

llm = get_default_text_generator(temperature=0.7, is_llm=False)

agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

def run_dungeon_master(prompt) -> str:
    """Run the dungeon master agent."""
    logger.info("Running dungeon_master.py")
    assert isinstance(prompt, str), "Prompt must be a string."
    if (len(prompt) < 1) or (len(prompt) > 1000):
        raise ValueError("Prompt must be at least 1 character or less than 1000 characters.")
    
    dm_result = agent_chain.run(prompt)
    logger.info(f"Finished running dungeon_master.py, result: {dm_result}")
    return dm_result

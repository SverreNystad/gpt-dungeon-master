from langchain import OpenAI
from langchain.tools import StructuredTool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
import logging
from src.npc_generation import generate_npc
from src.outcome_engine.referee import decide_difficulty
from src.text_generation.text_generator import get_default_text_generator

# Set up logging
logger = logging.getLogger(__name__)

# class DungeonMaster:

def fight():
    print("You fight the monster!")
    print("You win!")
    return "You win!"

def get_dungeon_master_template():
    """
    Return the dungeon master template.
    """
    dungeon_master_template = """
    You shall act as the narrator of the story. 
    You are in charge of the game world and the NPCs that inhabit it.
    You are also in charge of the rules of the game and the challenges that the players face.
    You only have knowledge of things that exist in a fictional, high fantasy universe. 
    You must not break character under any circumstances.
    Keep responses under 500 words. 
    Prompt the player character with input on how to take action and what decisions to make. 
    Do not make decisions for the player character.
    """

    return dungeon_master_template

def narrate(prompt: str) -> str:
    """
    Narrate the story based on the given prompt.
    """
    generator = get_default_text_generator(is_llm=False)
    # Give the dungeon master template to the generator first, so it can learn its role
    template = get_dungeon_master_template()
    generator.predict(template, True)
    narration = generator.predict(prompt)

    print(narration)
    return narration

tools = [
    StructuredTool.from_function(
        name= "NPC Generator", 
        func=generate_npc, 
        description="Generates a NPC based on the given prompt."
    ),
    StructuredTool.from_function(
        name = "Difficulty Analyzer",
        func=decide_difficulty,
        description="Decides the difficulty of the challenge the user tries to do based on the context. Values between 0 and 1, where 0 is trivial and 1 is nearly impossible."
    ),
    StructuredTool.from_function(
        name = "Narrator",
        func=narrate,
        description="Narrates the story based on the given prompt."
    ),
    StructuredTool.from_function(
        name = "Fight",
        func=fight,
        description="If there is any combat!"
    ),
]


memory = ConversationBufferMemory(memory_key="chat_history")
# llm = get_default_text_generator(temperature=0.7, is_llm=False)
llm = OpenAI(temperature=0)
agent_chain = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=False, 
    memory=memory,
    max_iterations=2,
    )

def run_dungeon_master(prompt) -> str:
    """Run the dungeon master agent."""
    if not isinstance(prompt, str):
        raise TypeError("Prompt must be a string.")

    if (len(prompt) < 1) or (len(prompt) > 1000):
        raise ValueError("Prompt must be at least 1 character or less than 1000 characters.")
    
    dm_result = agent_chain.run(prompt)
    logger.info(f"Finished running dungeon_master.py, result: {dm_result}")
    return dm_result

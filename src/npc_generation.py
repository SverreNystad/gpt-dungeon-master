from dataclasses import dataclass
from langchain.llms import OpenAI
# from langchain.chat_models import OpenAI
from enum import Enum
from src.text_generation.config import GPTConfig
from langchain.schema import HumanMessage



class Race(Enum):
    HUMAN = "human"
    ELF = "elf"
    DWARF = "dwarf"
    HALF_ELF = "half elf"
    DRAGONBORN = "dragonborn"
    GNOME = "gnome"
    HALF_ORC = "half orc"
    TIEFLING = "tiefling"
    HAFLING = "hafling"

class Alignment(Enum):
    LAWFUL_GOOD = "lawful good"
    NEUTRAL_GOOD = "neutral good"
    CHAOTIC_GOOD = "chaotic good"
    LAWFUL_NEUTRAL = "lawful neutral"
    NEUTRAL = "neutral"
    CHAOTIC_NEUTRAL = "chaotic neutral"
    LAWFUL_EVIL = "lawful evil"
    NEUTRAL_EVIL = "neutral evil"
    CHAOTIC_EVIL = "chaotic evil"


@dataclass()
class NPC:
    """Class for non-player characters (NPCs)."""
    # NPC PROFILE
    name: str
    age: int
    race: Race
    occupation: str
    alignment: Alignment
    
    # NPC STATS

def generate_npc() -> NPC:
    """Generate an NPC."""

    api_key = GPTConfig.API_KEY
    llm = OpenAI(openai_api_key=api_key)
    text = "What would be a good name for a elf wizard for a RPG?"

    # messege = [HumanMessage(content=text)]
    name: str = llm.predict(text)
    title: str = "The Wizard"
    return name





def generate_dummy_npc() -> NPC:
    good_human = NPC("Rolf", 20, Race.HUMAN, "farmer", Alignment.NEUTRAL_GOOD)

    bad_half_orc = NPC("Mort", 40, Race.HALF_ORC, "bandit", Alignment.CHAOTIC_EVIL)
    
    print(f"good_human {good_human}")
    print(f"bad_half_orc {bad_half_orc}")
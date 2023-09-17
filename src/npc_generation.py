from dataclasses import dataclass
import random
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from enum import Enum
from src.text_generation.config import GPTConfig
from langchain.schema import HumanMessage


api_key = GPTConfig.API_KEY
llm = OpenAI(openai_api_key=api_key)
chat_model = ChatOpenAI(openai_api_key=api_key)


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
class NPCProfile:
    """The  for non-player characters (NPCs)."""
    name: str
    age: int
    race: Race
    alignment: Alignment
    alive: bool
    background: str

@dataclass()
class NPCRelations:
    """The relations for non-player characters (NPCs)."""
    list_of_relations: list[str]

@dataclass()
class NPCRelation:
    name: str
    type_of_relation: str
    attitude: float
    still_exist: bool

@dataclass()
class NPC:
    """Class for non-player characters (NPCs)."""
    # NPC PROFILE
    NPCProfile: NPCProfile
    

    # occupation: str
    # relations: list[str] 

    # NPC STATS

def generate_npc() -> NPC:
    """Generate an NPC."""
    age: int = 20
    race: Race = Race.HALF_ELF
    role: str = "Shopkeeper"

    text = f"What would be a good name for a {race.value} that has the role of {role} for a RPG?"
    name: str = llm.predict(text)

    background = generate_general_background(name, age, race, role)
    alignment = generate_alignment(background)

    return NPC(NPCProfile(name, age, race, alignment, True, background))
    


def generate_alignment(info:str=None, alignment_list:list[Alignment]=[]) -> Alignment:
    alignment_template = "What is the alignment of the NPC?"
    if info is not None:
        alignment_template += f" Based on this info: {info}."
    else:
        return random.choice(Alignment)
    if len(alignment_list) == 0:
        alignment_list = [alignment.value for alignment in Alignment]
    alignment_template += f" It must be one of the following: {alignment_list}, do not give any other answer."
    alignment = llm.predict(alignment_template)
    print(alignment_template)
    if alignment not in alignment_list:
        return generate_alignment(info, alignment_list)
    return alignment

def generate_general_background(name: str, age: int, race: Race, role: str) -> str:
    """Generate a background for an NPC."""
    
    text = f"""Generate a backstory for a NPC of race: {race.value}, with the name: {name}, and age: {age}. The character should have the role: {role} in the story.
    """
    return llm.predict(text)
    

def generate_dummy_npc() -> NPC:
    good_human = NPC("Rolf", 20, Race.HUMAN, "farmer", Alignment.NEUTRAL_GOOD)

    bad_half_orc = NPC("Mort", 40, Race.HALF_ORC, "bandit", Alignment.CHAOTIC_EVIL)
    

    
    print(f"good_human {good_human}")
    print(f"bad_half_orc {bad_half_orc}")
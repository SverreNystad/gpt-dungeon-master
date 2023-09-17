from dataclasses import dataclass
from langchain.llms import OpenAI
from langchain.llms import OpenAI
from enum import Enum

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
    
    name: str
    age: int
    race: Race
    occupation: str
    alignment: Alignment
    

def generate_npc() -> NPC:
    """Generate an NPC."""
    pass
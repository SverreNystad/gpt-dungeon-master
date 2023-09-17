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

@dataclass()
class NPC:
    """Class for non-player characters (NPCs)."""
    
    name: str
    age: int
    race: Race
    occupation: str
    
    

def generate_npc() -> NPC:
    """Generate an NPC."""
    pass
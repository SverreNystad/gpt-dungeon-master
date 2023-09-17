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
class NPCPsychology:
    """The psychology for non-player characters (NPCs)."""
    personality: str
    ideals: list[str]
    bonds: list[str]
    flaws: list[str]
    goals: list[str]
    fears: list[str]
    interests: list[str]

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
    relations: NPCRelations 
    psychology: NPCPsychology
    # occupation: str

    # NPC STATS

def generate_npc() -> NPC:
    """Generate an NPC."""
    age: int = 20
    race: Race = Race.HALF_ELF
    role: str = "Shopkeeper"

    name_template = f"What would be a good name for a {race.value} that has the role of {role} for a RPG?"
    name: str = llm.predict(name_template)

    background = generate_general_background(name, age, race, role)
    alignment = generate_alignment(background)
    profile = NPCProfile(name, age, race, alignment, True, background)

    relations: NPCRelations = generate_npc_relations(background)
    psychology: NPCPsychology = generate_npc_psychology(profile, background, relations)
    return NPC(profile, relations, psychology)
    
def generate_general_background(name: str, age: int, race: Race, role: str) -> str:
    """
    Generate a background for an NPC.

    Args:
        name (str): The name of the NPC.
        age (int): The age of the NPC.
        race (Race): The race of the NPC.
        role (str): The role of the NPC in the story.
    Returns:
        str: The background of the NPC.
    """
    
    text = f"""Generate a backstory for a NPC of race: {race.value}, with the name: {name}, and age: {age}. The character should have the role: {role} in the story."""
    background = llm.predict(text)
    return background

def generate_alignment(info:str=None, alignment_list:list[Alignment]=None) -> Alignment:
    if info is None:
        return random.choice(Alignment)
    if alignment_list is None:
        alignment_list = [alignment.value for alignment in Alignment]

    alignment_template = get_alignment_template(info, alignment_list)
    raw_alignment = llm.predict(alignment_template)
    
    # Clean the alignment
    alignment = raw_alignment.replace("\n", "")
    alignment = alignment.lower()
    return alignment

def get_alignment_template(info:str=None, alignment_list:list[Alignment]=[]) -> str:
    """Get the template for the alignment question.
    Args:
        info (str, optional): Information about the NPC. Defaults to None.
        alignment_list (list[Alignment], optional): List of alignments that are allowed. Defaults to all possible alignments.
    Returns:
        str: The template for the alignment question.
    """
    alignment_template = "What is the alignment of the NPC?"
    if info is not None:
        alignment_template += f" Based on this info: {info}."
    if len(alignment_list) == 0:
        alignment_list = [alignment.value for alignment in Alignment]
    alignment_template += f" It must be one of the following: {alignment_list}, do not give any other answer."
    return alignment_template

def generate_npc_relations(background:str) -> NPCRelations:
    """Generate the relations for an NPC."""
    # Generate relations
    relations_template = get_npc_relation_template(background)
    raw_relations = llm.predict(relations_template)
    
    # Clean the relations
    raw_relations = raw_relations.strip()
    relations: list[str] = raw_relations.split("\n")

    # Create NPCRelations object
    different_relations: list[NPCRelation] = []
    for raw_relation in relations:
        # raw_relation format: [name], [type_of_relation], [attitude], [still_exist]
        relation = raw_relation.split(",")
        name: str = relation[0].strip()
        type_of_relation: str = relation[1].strip()
        attitude: float = relation[2].strip()
        still_exist: bool = relation[3].strip()

        different_relations.append(NPCRelation(name, type_of_relation, attitude, still_exist))

    return NPCRelations(different_relations)

def get_npc_relation_template(background: str) -> str:
    """Get the template for the NPC relation question."""
    npc_relation_template = (
        f"Generate relations for an NPC given its background: {background}. A relation should be in the format: "
        "'[name], [type_of_relation], [attitude], [still_exist]'\n"
        "[name]: Replace with the name of the other NPC to whom the main NPC has a relation.\n"
        "[type_of_relation]: Replace with the type of relation the main NPC has with the other NPC (e.g., friend, enemy, acquaintance, sibling, spouse).\n"
        "[attitude]: Replace with a float value between -1 and 1 (where -1 is extreme hatred and 1 is extreme love) indicating the main NPC's attitude towards the other NPC.\n"
        "[still_exist]: Replace with a boolean value (True or False) indicating if the relationship still exists."
        "The relations should be separated by a new line. Do not give any other answer."
    )
    return npc_relation_template

def generate_npc_psychology(profile: NPCProfile, background: str, relations: NPCRelations) -> NPCPsychology:
    """Generate the psychology for an NPC."""
    # Generate psychology
    psychology_template = get_psychology_template(profile, background, relations)
    raw_psychology = llm.predict(psychology_template)
    
    # Clean the psychology
    raw_psychology = raw_psychology.strip()
    print(raw_psychology)

    # Create NPCPsychology object
    psychology = raw_psychology.split(" | ")
    personality_traits: list[str] = psychology[0]
    # Format: [personality] | [ideals] | [bonds] | [flaws] | [goals] | [fears] | [interests]
    ideals: list[str] = psychology[1]
    bonds: list[str] = psychology[2]
    flaws: list[str] = psychology[3]
    goals: list[str] = psychology[4]
    fears: list[str] = psychology[5]
    interests: list[str] = psychology[6]

    return NPCPsychology(personality_traits, ideals, bonds, flaws, goals, fears, interests)

def get_psychology_template(profile: NPCProfile, background: str, relations: NPCRelations) -> str:
    psychology_template = f"""
        NPC Characteristics:
        - Background: {background}
        - Race: {profile.race}
        - Age: {profile.age}
        - Alignment: {profile.alignment}
        - Relations: {relations}

        Please generate an NPC psychological profile using the format:
        '[personality] | [ideals] | [bonds] | [flaws] | [goals] | [fears] | [interests]'
        Do not give any other answer."""
    return psychology_template

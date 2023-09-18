from dataclasses import dataclass
import random
from langchain.llms import OpenAI
from enum import Enum
from src.text_generation.config import GPTConfig
from langchain.schema import HumanMessage


api_key = GPTConfig.API_KEY
llm = OpenAI(openai_api_key=api_key)


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

class LifeStage(Enum):
    CHILD = "child"
    ADOLESCENT = "adolescent"
    YOUNG_ADULT = "young adult"
    ADULT = "adult"
    MIDDLE_AGE = "middle age"
    OLD = "old"

@dataclass()
class Age:
    years_old: int
    life_stage: LifeStage

class Alignment(Enum):
    """
    An enumeration representing the nine classic alignments found in role-playing games.
    
    These alignments define a character's moral and ethical compass, and are often used 
    to depict a character's personal beliefs and tendencies.
    """

    LAWFUL_GOOD = "lawful good" 
    """Characters believe in order and doing what's right."""
    NEUTRAL_GOOD = "neutral good"
    """Characters do the best they can to help others, without bias."""
    CHAOTIC_GOOD = "chaotic good"
    """Characters act as their conscience directs, with little regard for rules."""
    LAWFUL_NEUTRAL = "lawful neutral"
    """Characters act in accordance with law, order, and tradition."""
    NEUTRAL = "neutral"
    """Characters are indifferent and act without prejudice or compulsion."""
    CHAOTIC_NEUTRAL = "chaotic neutral"
    """Characters follow their whims and are essentially unpredictable."""
    LAWFUL_EVIL = "lawful evil"
    """Characters take what they want through authority, no matter the cost."""
    NEUTRAL_EVIL = "neutral evil"
    """Characters do whatever they can to gain, without any moral compass."""
    CHAOTIC_EVIL = "chaotic evil"
    """Characters act with malice, disregarding any semblance of order."""

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
    appearance: str
    # occupation: str

    # NPC STATS

def generate_npc() -> NPC:
    """Generate an NPC."""
    race: Race = Race.HALF_ELF
    role: str = "Shopkeeper"
    age: int = generate_age_for_race(race)

    name = generate_name(race, role)

    background = generate_general_background(name, age, race, role)
    alignment = generate_alignment(background)
    profile = NPCProfile(name, age, race, alignment, True, background)

    relations: NPCRelations = generate_npc_relations(background)
    psychology: NPCPsychology = generate_npc_psychology(profile, background, relations)

    appearance = generate_appearance(race, age, role, background)
    return NPC(profile, relations, psychology, appearance)

def generate_name(race: Race, role: str) -> str:
    name_template = f"What would be a good name for a {race.value} that has the role of {role} for a RPG?"
    raw_name: str = llm.predict(name_template)
    # Clean the name
    name = raw_name.replace("\n", "")
    return name

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
        try:
            relation = raw_relation.split(",")
            name: str = relation[0].strip()
            type_of_relation: str = relation[1].strip()
            attitude: float = relation[2].strip()
            still_exist: bool = relation[3].strip()
            different_relations.append(NPCRelation(name, type_of_relation, attitude, still_exist))
        except IndexError:
            print(f"Error: {raw_relation} is not a valid relation.")


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
    """
    Get the template for the NPC psychology question.
    
    Args:
        profile (NPCProfile): The profile of the NPC.
        background (str): The background of the NPC.
        relations (NPCRelations): The relations of the NPC.
    Returns:
        str: The template for the NPC psychology question.
    """
    psychology_template = f"""
        NPC Characteristics:
        - Background: {background}
        - Race: {profile.race}
        - Age: {profile.age}
        - Alignment: {profile.alignment}
        - Relations: {relations}

        Please generate an NPC psychological profile using the format:
        '[personality] | [ideals] | [bonds] | [flaws] | [goals] | [fears] | [interests]'
        Do not give any other answer and only give the values."""
    return psychology_template

def generate_age_for_race(race: Race) -> int:
    """
    Generate age based on race.

    Args:
        race (Race): The race of the character.
    Returns:
        int: The age of the character.
    """
    # TODO: REFACTOR MAKE USE OF MATCH CASE
    if race == Race.HUMAN:
        human_max_age = 90
        human_min_age = 6
        age = random.randint(human_min_age, human_max_age)

    elif race == Race.ELF:
        elf_max_age = 750
        elf_min_age = 6
        age = random.randint(elf_min_age, elf_max_age)
    elif race == Race.DWARF:
        dwarf_max_age = 350
        dwarf_min_age = 6
        age = random.randint(dwarf_min_age, dwarf_max_age)
    elif race == Race.HALF_ELF:
        half_elf_max_age = 180
        half_elf_min_age = 6
        age = random.randint(half_elf_min_age, half_elf_max_age)
    elif race == Race.DRAGONBORN:
        dragonborn_max_age = 80
        dragonborn_min_age = 1
        age = random.randint(dragonborn_min_age, dragonborn_max_age)
    elif race == Race.GNOME:
        gnome_max_age = 500
        gnome_min_age = 6
        age = random.randint(gnome_min_age, gnome_max_age)
    elif race == Race.HALF_ORC:
        half_orc_max_age = 75
        half_orc_min_age = 1
        age = random.randint(half_orc_min_age, half_orc_max_age)
    elif race == Race.TIEFLING:
        tiefling_max_age = 100
        tiefling_min_age = 6
        age = random.randint(tiefling_min_age, tiefling_max_age)
    elif race == Race.HAFLING:
        halfling_max_age = 250
        halfling_min_age = 6
        age = random.randint(halfling_min_age, halfling_max_age)

    return age

def generate_appearance(race: Race, age: int, role: str, backstory: str) -> str:
    
    # Generate appearance
    appearance_template = get_appearance_template(race, age, role, backstory)
    raw_appearance = llm.predict(appearance_template)

    # Parse the appearance
    appearance = raw_appearance.strip()
    return appearance

def get_appearance_template(race: Race, age: int, role: str, story: str) -> str:
    """"Get the template for the appearance question."""

    # Physique & Build: {physique}
    # Facial Features: {facial_features}
    # Eye & Hair Color: {eye_hair_color}
    # Distinguishing Marks: {marks}
    # Clothing & Accessories: {clothing}
    # Posture & Gait: {posture}
    # Age & Aging Signs: {age_signs}
    # Race & Ethnic Features: {race_features}
    # Voice & Speech Pattern: {voice}
    # Other Notable Features: {other_features}
    appearance_template = f"""
        Using the details:
        Fantasy Race: {race.value}
        Age: {age}
        Role in Story: {role}
        Story Context: {story}

        Please generate an appearance description for the NPC.
        """
    return appearance_template
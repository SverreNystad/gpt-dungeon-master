import pytest
from src.npc_generation import Alignment, NPCProfile, NPCRelations, Race, get_alignment_template, get_appearance_template, get_npc_relation_template, get_psychology_template

@pytest.fixture
def ALL_ALIGNMENTS():
    return [alignment.value for alignment in Alignment]

def test_alignment_no_info_no_alignment_list_generate_for_all_alignments(ALL_ALIGNMENTS):
    # Arrange
    info = None
    alignment_list = []
    # Act
    alignment_template = get_alignment_template(info, alignment_list)
    expected_template = f"What is the alignment of the NPC? It must be one of the following: {ALL_ALIGNMENTS}, do not give any other answer."
    # Assert
    print(alignment_template)
    assert alignment_template == expected_template

def test_alignment_template():
    info = "A human that is a shopkeeper. That is a good person. The incarnation of good."
    good_alignment = [Alignment.LAWFUL_GOOD, Alignment.NEUTRAL_GOOD, Alignment.CHAOTIC_GOOD]
    alignment_template = get_alignment_template(info, good_alignment)
    assert alignment_template == f"What is the alignment of the NPC? Based on this info: {info}. It must be one of the following: {good_alignment}, do not give any other answer."


def test_get_npc_relation_template():
    background = "The NPC grew up in a small village."
    result = get_npc_relation_template(background)
    assert "Generate relations for an NPC given its background:" in result
    assert background in result
    assert "'[name], [type_of_relation], [attitude], [still_exist]'" in result
        
def test_get_psychology_template():
    profile = NPCProfile("John", 25, Race.HUMAN, Alignment.LAWFUL_GOOD, True, "He is a hero.")
    background = "John was born in a small town."
    relations = NPCRelations(["Sarah, friend, 1.0, True"])
    result = get_psychology_template(profile, background, relations)
    assert "Background:" in result
    assert "Race:" in result
    assert "Age:" in result
    assert "Alignment:" in result
    assert "Relations:" in result
    assert "Please generate an NPC psychological profile" in result
        
def test_get_appearance_template():
    race = Race.ELF
    age = 120
    role = "Mage"
    backstory = "This elf has been living in the forest for centuries."
    result = get_appearance_template(race, age, role, backstory)
    assert "Fantasy Race:" in result
    assert "Age:" in result
    assert "Role in Story:" in result
    assert "Story Context:" in result
    assert "Please generate an appearance description for the NPC." in result

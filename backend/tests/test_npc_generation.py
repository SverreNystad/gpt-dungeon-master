import pytest

from src.npc_generation import (
    NPC,
    Alignment,
    NPCProfile,
    NPCPsychology,
    NPCRelations,
    Race,
    generate_age_for_race,
    generate_alignment,
    generate_appearance,
    generate_general_background,
    generate_name,
    generate_npc,
    generate_npc_psychology,
    generate_npc_relations,
)


@pytest.mark.apitest
def test_generate_npc():
    npc = generate_npc()
    assert isinstance(npc, NPC), "generate_npc should return an instance of NPC"


@pytest.mark.apitest
def test_generate_name():
    for race in Race:
        name = generate_name(race, "Warrior")
        assert (
            isinstance(name, str) and len(name) > 0
        ), f"generate_name failed for race: {race}"


@pytest.mark.apitest
def test_generate_general_background():
    bg = generate_general_background("John", 25, Race.HUMAN, "Guard")
    assert (
        isinstance(bg, str) and len(bg) > 0
    ), "generate_general_background should return a non-empty string"


@pytest.mark.apitest
def test_generate_alignment_for_evil_characters():
    # Arrange
    info = "A human that is a shopkeeper. That is the incarnation of evil."
    evil_alignment = [
        Alignment.LAWFUL_EVIL,
        Alignment.NEUTRAL_EVIL,
        Alignment.CHAOTIC_EVIL,
    ]
    expected_alignment = [alignment.value for alignment in evil_alignment]
    # Act
    alignment = generate_alignment(info, evil_alignment)
    # Assert
    assert alignment in expected_alignment


@pytest.mark.apitest
def test_generate_npc_relations():
    relations = generate_npc_relations("John was a warrior who fought many battles.")
    assert isinstance(
        relations, NPCRelations
    ), "generate_npc_relations should return an instance of NPCRelations"


@pytest.mark.apitest
def test_generate_npc_psychology():
    profile = NPCProfile(
        name="John",
        age=25,
        race=Race.HUMAN,
        alignment=Alignment.NEUTRAL_GOOD,
        alive=True,
        background="A brave warrior.",
    )
    relations = NPCRelations(list_of_relations=[])
    psychology = generate_npc_psychology(profile, "John was a warrior", relations)
    assert isinstance(
        psychology, NPCPsychology
    ), "generate_npc_psychology should return an instance of NPCPsychology"


def test_generate_age_for_race():
    race_age_limits = {
        Race.HUMAN: (6, 90),
        Race.ELF: (6, 750),
        Race.DWARF: (6, 350),
        Race.HALF_ELF: (6, 180),
        Race.DRAGONBORN: (1, 80),
        Race.GNOME: (6, 500),
        Race.HALF_ORC: (1, 75),
        Race.TIEFLING: (6, 100),
        Race.HAFLING: (6, 250),
    }
    for race, (min_age, max_age) in race_age_limits.items():
        age = generate_age_for_race(race)
        assert (
            min_age <= age <= max_age
        ), f"generate_age_for_race failed for race: {race}"


@pytest.mark.apitest
def test_generate_appearance():
    appearance = generate_appearance(Race.HUMAN, 25, "Guard", "John was a brave guard.")
    assert (
        isinstance(appearance, str) and len(appearance) > 0
    ), "generate_appearance should return a non-empty string"

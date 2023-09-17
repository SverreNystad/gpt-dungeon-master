
import pytest
from src.npc_generation import Alignment, generate_alignment, get_alignment_template

@pytest.fixture
def ALL_ALIGNMENTS():
    return [alignment.value for alignment in Alignment]

# Alignment
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


@pytest.mark.apitest
def test_generate_alignment_for_evil_characters():
    # Arrange
    info = "A human that is a shopkeeper. That is the incarnation of evil."
    evil_alignment = [Alignment.LAWFUL_EVIL, Alignment.NEUTRAL_EVIL, Alignment.CHAOTIC_EVIL]
    expected_alignment = [alignment.value for alignment in evil_alignment]
    # Act
    alignment = generate_alignment(info, evil_alignment)
    # Assert
    assert alignment in expected_alignment
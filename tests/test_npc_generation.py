import pytest

from src.npc_generation import Alignment, generate_alignment

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
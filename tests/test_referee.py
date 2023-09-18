import pytest
from src.referee import Difficulty, decide_difficulty

@pytest.fixture
def TRIVIAL_CONTEXT():
    return """
    You are trying to walk down the street. 
    It is good weather and you are wearing comfortable shoes.
    The street is flat and there are no obstacles in your way.
    """

@pytest.fixture
def VERY_EASY_CONTEXT():
    return """
    You try to throw a ball into a basket a few meters away, but the sun is shining in your eyes.
    """

@pytest.fixture
def EASY_CONTEXT():
    return """
    An easy task.
    """

@pytest.fixture
def MEDIUM_CONTEXT():
    return "You are trying to climb a tree. The tree is not very tall and has many branches."

@pytest.fixture
def HARD_CONTEXT():
    return "You are trying to climb a tree. The tree is very tall and has few branches."

@pytest.fixture
def NEARLY_IMPOSSIBLE_CONTEXT():
    return """
    You are trying to climb a tree. In a storm. The tree is very tall and no branches.
    The tree is also covered in oil. And you are wearing a heavy backpack.
    """

contexts = [
    (TRIVIAL_CONTEXT, Difficulty.TRIVIAL.value, Difficulty.VERY_EASY.value),
    (VERY_EASY_CONTEXT, Difficulty.TRIVIAL.value, Difficulty.EASY.value),
    (EASY_CONTEXT, Difficulty.VERY_EASY.value, Difficulty.MEDIUM.value),
    (MEDIUM_CONTEXT, Difficulty.EASY.value, Difficulty.HARD.value),
    (HARD_CONTEXT, Difficulty.MEDIUM.value, Difficulty.NEARLY_IMPOSSIBLE.value)
]

@pytest.mark.apitest
@pytest.mark.parametrize("context, expected_min_difficulty, expected_max_difficulty", contexts)
def test_decide_difficulty(context, expected_min_difficulty, expected_max_difficulty):
    # Arrange (already done by the parameters)
    # Act
    difficulty = decide_difficulty(context)
    # Assert
    assert difficulty >= expected_min_difficulty, "Difficulty was lower than the minimum"
    assert difficulty <= expected_max_difficulty, "Difficulty was higher then the maximum"

from enum import Enum
from src.text_generation.text_generator import get_default_text_generator


class Difficulty(Enum):
    """The difficulty of a action or task."""

    TRIVIAL = 0.0
    """Tasks of this difficulty are trivial for adventurers of any skill."""
    VERY_EASY = 0.1
    """Tasks of this difficulty are trivial for adventurers of almost any skill."""
    EASY = 0.3
    """A task of this difficulty is easy for adventurers of an appropriate skill."""
    MEDIUM = 0.5
    """A task of this difficulty is a challenge for adventurers of an appropriate skill."""
    HARD = 0.7
    """A task of this difficulty is difficult for adventurers of an appropriate skill."""
    VERY_HARD = 0.9
    """A task of this difficulty is very difficult for adventurers of an appropriate skill."""
    NEARLY_IMPOSSIBLE = 1.0
    """A task of this difficulty is almost impossible for adventurers of an appropriate skill."""


def decide_difficulty(context: str) -> float:
    """Decide the difficulty of the challenge based on the context."""

    prompt = get_difficulty_template(context)
    raw_difficulty = get_default_text_generator().predict(prompt)
    print(raw_difficulty)
    difficulty = float(raw_difficulty)
    return difficulty


def get_difficulty_template(context: str) -> str:
    """Return the difficulty template for the given difficulty."""

    difficulty_template = f"""
    Based on the context: {context}, the difficulty of the challenge is:
    '[difficulty]'\n
    [difficulty] is a float between 0 and 1, where 0 is trivial and 1 is nearly impossible.
    Do not answer with anything else then a number between 0 and 1.
    """
    return difficulty_template

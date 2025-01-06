import random
from typing import Tuple

class AbilityCheck:
    # Class-level dictionary for abilities and difficulty classes
    ABILITIES = {
        "Strength": "measuring physical power",
        "Dexterity": "measuring agility",
        "Constitution": "measuring endurance",
        "Intelligence": "measuring reasoning and memory",
        "Wisdom": "measuring perception and insight",
        "Charisma": "measuring force of personality"
    }
    
    DIFFICULTY_CLASSES = {
        "Very Easy": 5,
        "Easy": 10,
        "Medium": 15,
        "Hard": 20,
        "Very Hard": 25,
        "Nearly Impossible": 30
    }

    def __init__(self, task_name: str, ability:str, difficulty:str):
        """
        Initialize an ability check for a specific task.

        Args:
            task_name [str]: Description of the task.
            ability [str]: One of the six abilities from AbilityCheck.Abilities required for the task.
            difficulty [str]: The difficulty of the task represented by one the Difficulty classes (DC) 
            from AbilityCheck.DIFFICULTY_CLASSES
        """
        if ability not in self.ABILITIES:
            raise ValueError(f"Invalid ability. Choose from: {', '.join(self.ABILITIES.keys())}")
        if difficulty not in self.DIFFICULTY_CLASSES.values():
            raise ValueError(f"Invalid difficulty class. Valid values: {list(self.DIFFICULTY_CLASSES.values())}")
        
        self.task_name = task_name
        self.ability = ability
        self.difficulty = difficulty



    def make_check(self, ability_modifier: int, bonuses=0, penalties=0) -> Tuple[bool, int, int]:
        """
        Perform the ability check by rolling a d20 and adding modifiers.

        Args:
            ability_modifier [int]: The character's ability modifier for the relevant ability.
            bonuses [int]: Any additional bonuses to the roll (default: 0).
            penalties [int]: Any penalties to the roll (default: 0).

        Return:
            Tuple (success: bool, roll_result: int, total_score: int)
        """
        roll = random.randint(1, 20)
        total_score = roll + ability_modifier + bonuses - penalties
        success = total_score >= self.difficulty
        return success, roll, total_score

    def __str__(self):
        """String representation of the ability check task."""
        difficulty_name = next((name for name, dc in self.DIFFICULTY_CLASSES.items() if dc == self.difficulty), "Unknown")
        return f"Task: {self.task_name}\nAbility: {self.ability} ({self.ABILITIES[self.ability]})\nDifficulty: {difficulty_name} (DC {self.difficulty})"

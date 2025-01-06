
from knowledge_base.agent.rag_service import lookup_rules

def test_rules_lookup():
    description = "You are in a dark cave, and you hear a loud growl coming from the darkness"
    character = "The player is a level 5 wizard with a intelligence of 18, wisdom of 12, and a charisma of 14, and a spellbook with the following spells: fireball, magic missile, and shield"
    player_action = "The player casts fireball at the growling sound"
    context = f"{description} {character} {player_action}"

    rules = lookup_rules(context)

    print(rules)

def test_narrative_given_rules():
    rules = """
    {
        "context": {
            "environment": "dark cave",
            "situation": "loud growl from darkness",
            "player": {
            "class": "wizard",
            "level": 5,
            "ability_scores": {
                "intelligence": 18,
                "wisdom": 12,
                "charisma": 14
            },
            "spellbook": [
                "fireball",
                "magic missile",
                "shield"
            ]
            },
            "action": "cast fireball"
        },
        "rules": {
            "spellcasting": {
            "spell": "fireball",
            "level": 3,
            "casting_time": "1 action",
            "range": "150 feet",
            "components": {
                "verbal": true,
                "somatic": true,
                "material": {
                "type": "a tiny ball of bat guano and sulfur"
                }
            },
            "duration": "instantaneous",
            "effect": {
                "description": "A bright streak flashes from your pointing finger to a point you choose within range and then blossoms with a low roar into an explosion of flame.",
                "area_of_effect": "20-foot radius sphere",
                "damage": {
                "type": "fire",
                "dice": "8d6",
                "saving_throw": {
                    "type": "Dexterity",
                    "DC": "8 + your proficiency bonus + your Intelligence modifier",
                    "success": "half damage"
                }
                }
            }
            },
            "spell_save_dc": {
            "calculation": "8 + proficiency bonus + Intelligence modifier",
            "proficiency_bonus": 3,
            "intelligence_modifier": 4,
            "dc": 15
            },
            "darkvision": {
            "description": "You can see in dim light within 60 feet of you as if it were bright light, and in darkness as if it were dim light. You can’t discern color in darkness, only shades of gray."
            }
        }
    }
    """
    
    


if __name__ == "__main__":
    
    test_narrative_given_rules()

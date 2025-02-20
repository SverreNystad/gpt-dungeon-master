
from knowledge_base.agent.rag_service import RagService
import optuna
import optunahub
from optuna.study import StudyDirection
from optuna_dashboard import run_server
import logging
import sys


def test_rules_lookup():
    description = "You are in a dark cave, and you hear a loud growl coming from the darkness"
    character = "The player is a level 5 wizard with a intelligence of 18, wisdom of 12, and a charisma of 14, and a spellbook with the following spells: fireball, magic missile, and shield"
    player_action = "The player casts fireball at the growling sound"
    context = f"{description} {character} {player_action}"

    rules = lookup_rules(context)

    print(rules)


def test_rules_lookup_ability_check():
    description = "You are in a dark cave, and you see a boulder the size of you blocking the path"
    character = "The player is a level 5 wizard with a strength of 8, intelligence of 18, wisdom of 12, and a charisma of 14, and a spellbook with the following spells: fireball, magic missile, and shield"
    player_action = "The player tries to lift the boulder blocking the path"
    context = f"{description} {character} {player_action}"

    rules = lookup_rules(context)

    print(rules)


def test_rules_lookup_fighter_figthing():
    description = "You are on a battlefield, and you see a goblin charging at you"
    character = "The player is a level 1 fighter with a strength of 8, intelligence of 18, wisdom of 12, and a charisma of 14. The player is wearing a chainmail armor and has a longsword and a shield"
    player_action = "The player tries to fight the goblin"
    context = f"{description} {character} {player_action}"

    rules_1 = lookup_rules(context)
    rules_2 = lookup_rules_v2(context)

    print(rules_1)
    print("\n\n\n\n")
    print(rules_2)


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
    
async def test_faithfullness():
    from ragas.dataset_schema import SingleTurnSample 
    from ragas.metrics import Faithfulness
    sample = SingleTurnSample(
        user_input="What ability scores do Dragonborn gain?",
        response="Dragonborn gain the following ability scores: their Strength score increases by 2, and their Charisma score increases by 1.",
        retrieved_contexts=[
            """## Dragonborn {#section-dragonborn}

### Dragonborn Traits

Your draconic heritage manifests in a variety of traits you share with other dragonborn.

***Ability Score Increase.*** Your Strength score increases by 2, and your Charisma score increases by 1."""
        ]
    )
    scorer = Faithfulness()
    await scorer.single_turn_ascore(sample)

def objective2(trial: optuna.Trial) -> float:
    nr_md_splitts = trial.suggest_int("md_splits", 1, 6)
    chunk_size = trial.suggest_int("chunk_size", 200, 1200)
    if chunk_size < 400:
        max_chunk_overlap = chunk_size - 1
    else:
        max_chunk_overlap = 500

    chunk_overlap = trial.suggest_int("chunk_overlap", 0, max_chunk_overlap)
    bm25_k = trial.suggest_int("bm25_k", 1, 25)
    bm25_weight = trial.suggest_float("bm25_weight", 0.0, 1.0)

    rag_service: RagService = RagService(
        nr_md_splitts = nr_md_splitts,
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        bm25_k = bm25_k,
        bm25_weight = bm25_weight)
    
    context_recall, context_precision, context_entity_recall = rag_service.rag_evaluator()
     
    del rag_service
    print(f"Context recall: {context_recall}")

    return context_recall, context_precision


def objective(trial: optuna.Trial) -> float:
    vector_k = trial.suggest_int("vector_k", 1, 20)
    breakpoint_threshold = trial.suggest_int("breakpoint_threshold",low=50,high=99, step=0.1)
    # if chunk_size < 500:
    #     max_chunk_overlap = chunk_size - 1
    # else:
    #     max_chunk_overlap = 500

    score_threshold = trial.suggest_float("score_threshold", 0.3, 0.75)
    bm25_k = trial.suggest_int("bm25_k", 1, 25)
    bm25_weight = trial.suggest_float("bm25_weight", 0.0, 1.0)
    md_splits = trial.suggest_int("md_splits", 2, 5)

    rag_service: RagService = RagService(
        vector_k= vector_k,
        breakpoint_threshold=breakpoint_threshold,
        score_threshold=score_threshold,
        bm25_k = bm25_k,
        bm25_weight = bm25_weight,
        md_splits=md_splits
        )
    context_recall, context_precision, context_entity_recall = rag_service.rag_evaluator()
     
    del rag_service
    print(f"Context recall: {context_recall}")

    return context_recall, context_precision, context_entity_recall

if __name__ == "__main__":
    # optuna.logging.get_logger("optuna").addHandler(logging.StreamHandler(sys.stdout))
    # study_name = "rag_builder_Parent_BM25" 
    # storage_name = "sqlite:///{}.db".format(study_name)
    # module = optunahub.load_module(package="samplers/auto_sampler")
    # directions = [StudyDirection.MAXIMIZE, StudyDirection.MAXIMIZE, StudyDirection.MAXIMIZE]

    # file_path = "knowledge_base/optuna_data/optuna_journal_storage.log"
    # lock_obj = optuna.storages.journal.JournalFileOpenLock(file_path)

    # storage = optuna.storages.JournalStorage(
    #     optuna.storages.journal.JournalFileBackend(file_path, lock_obj=lock_obj),
    # )

    

    # run_server(storage_name)
    # for _ in range(10):
    #     study.optimize(objective2, n_trials=10)

    # study = optuna.create_study(
    #     study_name=study_name,
    #     sampler=module.AutoSampler(),
    #     storage=storage_name,
    #     load_if_exists= True,
    #     directions=directions
    #     )
    
    # for _ in range(10):
    #      study.optimize(objective, n_trials=5)
    # run_server(storage_name)

    rag_service: RagService = RagService(
        vector_k=13,
        breakpoint_threshold=98,
        score_threshold=0.596,
        bm25_k = 12,
        bm25_weight = 0.02687,
        md_splits=2
        )
    
    # while(True):
    #     query = input("Question: ")
    #     print(rag_service.ask_model(query=query))


    print(rag_service.rag_evaluator())
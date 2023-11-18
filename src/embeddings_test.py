from openai.embeddings_utils import get_embedding
from langchain.memory import ConversationBufferMemory

from src.npc_generation import NPC


def generate_npc_embedding(npc: NPC) -> list:
    """
    Generates an embedding for the given NPC.
    """
    # You might want to customize what aspects of the NPC are used for the embedding
    npc_description = f"{npc.NPCProfile.name} {npc.appearance} {npc.NPCProfile.race} {npc.NPCProfile.alignment} {npc.psychology.personality}"
    return get_embedding(npc_description)


import json

npc_database = {}

def store_npc(npc: NPC, embedding: list):
    """
    Store the NPC and its embedding.
    """
    npc_database[npc.NPCProfile.name] = {"npc": npc, "embedding": embedding}

    # Optionally, save to a file
    with open("npc_database.json", "w") as file:
        json.dump(npc_database, file)


from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def retrieve_npc(query: str) -> NPC:
    """
    Retrieve the most similar NPC based on the query.
    """
    query_embedding = get_embedding(query)
    similarities = {}

    for npc_name, data in npc_database.items():
        sim = cosine_similarity(np.array(query_embedding).reshape(1, -1), np.array(data["embedding"]).reshape(1, -1))[0][0]
        similarities[npc_name] = sim

    most_similar_npc_name = max(similarities, key=similarities.get)
    return npc_database[most_similar_npc_name]["npc"]

def update_conversation_with_npc(memory: ConversationBufferMemory, npc: NPC):
    """
    Update the conversation memory with the NPC.
    """
    # Here, you'd add logic to store the NPC reference in the conversation
    memory.update({"npc_reference": npc.NPCProfile.name})


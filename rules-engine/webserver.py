from typing import Union
from fastapi import FastAPI
from src.knowledge_base.agent.rag_service import RagService

app = FastAPI()

rag_service: RagService = RagService(
    vector_k=13,
    breakpoint_threshold=98,
    score_threshold=0.596,
    bm25_k=12,
    bm25_weight=0.02687,
    md_splits=2,
)


@app.get("/")
def hello_world():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/rules")
def rule_lookup(user_prompt: str):
    response = rag_service.query(user_prompt=user_prompt)
    return {response: "0"}

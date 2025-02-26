from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.knowledge_base.agent.rag_service import RagService

app = FastAPI(
    title="Rules Engine",
    description="The rules engine to retrieve correct rules to provide answers to user prompts",
    version="1.0.0",
)

# Allow CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


rag_service: RagService = RagService(
    vector_k=13,
    breakpoint_threshold=98,
    score_threshold=0.596,
    bm25_k=12,
    bm25_weight=0.02687,
    md_splits=2,
)


@app.post("/rules")
def rule_lookup(user_prompt: str):
    if user_prompt is None:
        raise HTTPException(status_code=400, detail="user_prompt is required")
    if len(user_prompt) == 0:
        raise HTTPException(status_code=400, detail="user_prompt cannot be empty")

    response = rag_service.query(user_prompt=user_prompt)
    return JSONResponse(content=response)

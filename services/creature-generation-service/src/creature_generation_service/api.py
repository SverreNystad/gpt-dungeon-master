from datetime import datetime
from fastapi import FastAPI
from loguru import logger
from uuid import uuid

from src.models import CreatureCreationRequestDto, Job, CreatureCreationStatus

app = FastAPI()


@app.post("/creatures")
def queue_creature_creation(
    request: CreatureCreationRequestDto,
) -> Job:
    """
    Endpoint to queue creature creation .
    Args:
        request (CreatureCreationRequestDto): The request containing the creature data.
    Returns:
        CreatureCreationResponse: accepted queue
    """
    # Validation of submission
    logger.info(f"Received request: {request}")

    # Enqueue job in Cache
    job_id = uuid()
    timestamp = datetime.now().timestamp()
    job = Job(
        job_id,
        CreatureCreationStatus.PENDING,
        timestamp,
        request.user_id,
    )
    

    logger.info(f"Created job: {job} and saved in redis")

    return job


@app.get("/creatures/{id}")
def fetch_creature(id):
    # Check status from redis
    # When complete return creature model urls
    pass

from uuid import uuid
from dataclasses import dataclass
from datetime import datatime
from pydantic import BaseModel, Field
from enum import StrEnum, auto


class CreatureCreationRequestDto(BaseModel):
    description: str
    reference_image: str | None


class CreatureCreationStatus(StrEnum):
    PENDING = auto()
    INTERMEDIATE = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()


class CreatureCreationResponse(BaseModel):
    job_id: str
    status: CreatureCreationStatus


@dataclass
class Job:
    job_id: uuid
    status: CreatureCreationStatus
    created_at: float
    by_user: uuid

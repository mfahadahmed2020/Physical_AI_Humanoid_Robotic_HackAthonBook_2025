from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Shared properties
class ProgressBase(BaseModel):
    user_id: int
    chapter_id: int
    status: str  # NOT_STARTED, IN_PROGRESS, COMPLETED
    completion_percentage: Optional[float] = 0.0  # Percentage completed (0.0 to 1.0)
    time_spent: Optional[int] = None  # Time spent in seconds
    assessment_scores: Optional[str] = None  # JSON string representing scores for chapter assessments
    simulation_attempts: Optional[str] = None  # JSON string representing summary of simulation attempts

# Properties to receive via API on creation
class ProgressCreate(ProgressBase):
    pass

# Properties to receive via API on update
class ProgressUpdate(BaseModel):
    status: Optional[str] = None
    completion_percentage: Optional[float] = None
    time_spent: Optional[int] = None
    assessment_scores: Optional[str] = None
    simulation_attempts: Optional[str] = None

class ProgressInDBBase(ProgressBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_accessed: Optional[datetime] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class Progress(ProgressInDBBase):
    pass
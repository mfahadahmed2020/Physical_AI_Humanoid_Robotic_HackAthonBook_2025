from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


# Assessment-related Pydantic models
class AssessmentBase(BaseModel):
    chapter_id: int
    title: str
    description: Optional[str] = None
    assessment_type: str  # QUIZ, EXERCISE, PROJECT, SIMULATION_TASK
    questions: List[Dict[str, Any]]  # List of questions with possible answers
    max_score: int = 100
    time_limit: Optional[int] = None  # Time limit in seconds (null if no limit)


class AssessmentCreate(AssessmentBase):
    pass


class AssessmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assessment_type: Optional[str] = None
    questions: Optional[List[Dict[str, Any]]] = None
    max_score: Optional[int] = None
    time_limit: Optional[int] = None


class AssessmentInDBBase(AssessmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Assessment(AssessmentInDBBase):
    pass


class AssessmentSubmissionBase(BaseModel):
    assessment_id: int
    user_id: int
    answers: List[Dict[str, Any]]  # User's answers to the questions


class AssessmentSubmissionCreate(AssessmentSubmissionBase):
    pass


class AssessmentSubmissionUpdate(BaseModel):
    answers: Optional[List[Dict[str, Any]]] = None


class AssessmentSubmissionInDBBase(AssessmentSubmissionBase):
    id: int
    score: Optional[int] = None
    status: str = "SUBMITTED"  # SUBMITTED, GRADED
    graded_at: Optional[datetime] = None
    feedback: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AssessmentSubmission(AssessmentSubmissionInDBBase):
    pass


# Response models for API endpoints
class AssessmentWithSubmissions(Assessment):
    submissions: List[AssessmentSubmission] = []


class SubmissionResult(BaseModel):
    id: int
    assessment_id: int
    user_id: int
    answers: List[Dict[str, Any]]
    score: int
    max_score: int
    percentage: float
    status: str
    graded_at: Optional[datetime] = None
    feedback: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

# This is the base model that other models will inherit from
Base = declarative_base()

# Common columns that can be inherited by other models
class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)

# Import SQLAlchemy models
from .user import User
from .chapter import TextbookChapter
from .progress import LearningProgress
from .assessment import Assessment, AssessmentSubmission

# Import Pydantic models
from .user_pydantic import User, UserCreate, UserUpdate, UserInDB
from .chapter_pydantic import TextbookChapter, TextbookChapterCreate, TextbookChapterUpdate
from .progress_pydantic import LearningProgress, LearningProgressCreate, LearningProgressUpdate
from .assessment_pydantic import Assessment, AssessmentCreate, AssessmentUpdate, AssessmentSubmission, AssessmentSubmissionCreate, AssessmentSubmissionUpdate

__all__ = [
    # SQLAlchemy models
    "Base",
    "BaseMixin",
    "User",
    "TextbookChapter",
    "LearningProgress",
    "Assessment",
    "AssessmentSubmission",

    # Pydantic models
    "User",
    "UserCreate",
    "UserUpdate",
    "UserInDB",
    "TextbookChapter",
    "TextbookChapterCreate",
    "TextbookChapterUpdate",
    "LearningProgress",
    "LearningProgressCreate",
    "LearningProgressUpdate",
    "Assessment",
    "AssessmentCreate",
    "AssessmentUpdate",
    "AssessmentSubmission",
    "AssessmentSubmissionCreate",
    "AssessmentSubmissionUpdate",
]
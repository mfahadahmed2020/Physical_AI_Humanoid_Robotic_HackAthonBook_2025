from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class LearningProgress(Base):
    __tablename__ = "learning_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    chapter_id = Column(Integer, ForeignKey("textbook_chapters.id"), nullable=False)
    status = Column(String, nullable=False)  # NOT_STARTED, IN_PROGRESS, COMPLETED
    completion_percentage = Column(Float, default=0.0)  # Percentage completed (0.0 to 1.0)
    time_spent = Column(Integer)  # Time spent in seconds
    last_accessed = Column(DateTime(timezone=True), onupdate=func.now())
    assessment_scores = Column(Text)  # JSON string representing scores for chapter assessments
    simulation_attempts = Column(Text)  # JSON string representing summary of simulation attempts
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="progress_records")
    chapter = relationship("TextbookChapter", back_populates="progress_records")
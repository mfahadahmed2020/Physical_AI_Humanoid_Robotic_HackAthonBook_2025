from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("textbook_chapters.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)  # Description of the assessment
    assessment_type = Column(String, nullable=False)  # QUIZ, EXERCISE, PROJECT, SIMULATION_TASK
    questions = Column(JSON)  # JSON field containing list of questions with possible answers
    max_score = Column(Integer, default=100)  # Maximum possible score
    time_limit = Column(Integer)  # Time limit in seconds (null if no limit)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    chapter = relationship("TextbookChapter", back_populates="assessments")
    submissions = relationship("AssessmentSubmission", back_populates="assessment")


class AssessmentSubmission(Base):
    __tablename__ = "assessment_submissions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    answers = Column(JSON)  # JSON field containing user's answers to the questions
    score = Column(Integer)  # Score achieved
    status = Column(String, default="SUBMITTED")  # SUBMITTED, GRADED
    graded_at = Column(DateTime(timezone=True))  # When the assessment was graded
    feedback = Column(Text)  # Feedback for the user
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    assessment = relationship("Assessment", back_populates="submissions")
    user = relationship("User", back_populates="assessments_submitted")
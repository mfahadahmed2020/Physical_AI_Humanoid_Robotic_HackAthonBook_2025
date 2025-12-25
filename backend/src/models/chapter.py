from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base
from ..utils.constants import ChapterLevel, TopicArea

class TextbookChapter(Base):
    __tablename__ = "textbook_chapters"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    content = Column(Text, nullable=False)  # Markdown content of the chapter
    level = Column(SQLEnum(ChapterLevel), nullable=False)  # FOUNDATION, INTERMEDIATE, ADVANCED
    topic_area = Column(SQLEnum(TopicArea), nullable=False)  # EMBODIED_INTELLIGENCE, SIMULATION, etc.
    estimated_reading_time = Column(Integer, nullable=False)  # In minutes
    order_index = Column(Integer, nullable=False)  # Position in the textbook sequence
    prerequisites = Column(Text)  # JSON string representing list of prerequisite chapters
    learning_objectives = Column(Text)  # JSON string representing list of learning objectives
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    progress_records = relationship("LearningProgress", back_populates="chapter")
    assessments = relationship("Assessment", back_populates="chapter")
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ..utils.constants import ChapterLevel, TopicArea

# Shared properties
class ChapterBase(BaseModel):
    title: str
    slug: str
    content: str  # Markdown content of the chapter
    level: ChapterLevel  # FOUNDATION, INTERMEDIATE, ADVANCED
    topic_area: TopicArea  # EMBODIED_INTELLIGENCE, SIMULATION, etc.
    estimated_reading_time: int  # In minutes
    order_index: int  # Position in the textbook sequence
    prerequisites: Optional[str] = None  # JSON string representing list of prerequisite chapters
    learning_objectives: Optional[str] = None  # JSON string representing list of learning objectives

# Properties to receive via API on creation
class ChapterCreate(ChapterBase):
    pass

# Properties to receive via API on update
class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    level: Optional[ChapterLevel] = None
    topic_area: Optional[TopicArea] = None
    estimated_reading_time: Optional[int] = None
    order_index: Optional[int] = None
    prerequisites: Optional[str] = None
    learning_objectives: Optional[str] = None

class ChapterInDBBase(ChapterBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Additional properties to return via API
class Chapter(ChapterInDBBase):
    pass
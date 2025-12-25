from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.chapter import TextbookChapter as ChapterModel
from ..models.chapter_pydantic import TextbookChapterCreate, TextbookChapterUpdate


class ChapterService:
    @staticmethod
    def get_chapter_by_id(db: Session, chapter_id: int) -> Optional[ChapterModel]:
        return db.query(ChapterModel).filter(ChapterModel.id == chapter_id).first()

    @staticmethod
    def get_chapter_by_slug(db: Session, slug: str) -> Optional[ChapterModel]:
        return db.query(ChapterModel).filter(ChapterModel.slug == slug).first()

    @staticmethod
    def get_chapters(
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        level: Optional[str] = None, 
        topic_area: Optional[str] = None
    ) -> List[ChapterModel]:
        query = db.query(ChapterModel).order_by(ChapterModel.order_index)
        
        if level:
            query = query.filter(ChapterModel.level == level)
        
        if topic_area:
            query = query.filter(ChapterModel.topic_area == topic_area)
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_chapters_count(db: Session) -> int:
        return db.query(func.count(ChapterModel.id)).scalar()

    @staticmethod
    def create_chapter(db: Session, chapter: TextbookChapterCreate) -> ChapterModel:
        db_chapter = ChapterModel(
            title=chapter.title,
            slug=chapter.slug,
            content=chapter.content,
            level=chapter.level.value if hasattr(chapter.level, 'value') else chapter.level,
            topic_area=chapter.topic_area.value if hasattr(chapter.topic_area, 'value') else chapter.topic_area,
            estimated_reading_time=chapter.estimated_reading_time,
            order_index=chapter.order_index,
            prerequisites=chapter.prerequisites,
            learning_objectives=chapter.learning_objectives
        )
        
        db.add(db_chapter)
        db.commit()
        db.refresh(db_chapter)
        
        return db_chapter

    @staticmethod
    def update_chapter(db: Session, chapter_id: int, chapter_update: TextbookChapterUpdate) -> Optional[ChapterModel]:
        db_chapter = db.query(ChapterModel).filter(ChapterModel.id == chapter_id).first()
        
        if not db_chapter:
            return None

        # Update fields if provided
        if chapter_update.title:
            db_chapter.title = chapter_update.title
        if chapter_update.slug:
            db_chapter.slug = chapter_update.slug
        if chapter_update.content:
            db_chapter.content = chapter_update.content
        if chapter_update.level:
            db_chapter.level = chapter_update.level.value if hasattr(chapter_update.level, 'value') else chapter_update.level
        if chapter_update.topic_area:
            db_chapter.topic_area = chapter_update.topic_area.value if hasattr(chapter_update.topic_area, 'value') else chapter_update.topic_area
        if chapter_update.estimated_reading_time is not None:
            db_chapter.estimated_reading_time = chapter_update.estimated_reading_time
        if chapter_update.order_index is not None:
            db_chapter.order_index = chapter_update.order_index
        if chapter_update.prerequisites is not None:
            db_chapter.prerequisites = chapter_update.prerequisites
        if chapter_update.learning_objectives is not None:
            db_chapter.learning_objectives = chapter_update.learning_objectives
        
        db.commit()
        db.refresh(db_chapter)
        
        return db_chapter

    @staticmethod
    def delete_chapter(db: Session, chapter_id: int) -> bool:
        db_chapter = db.query(ChapterModel).filter(ChapterModel.id == chapter_id).first()
        
        if not db_chapter:
            return False

        db.delete(db_chapter)
        db.commit()
        
        return True
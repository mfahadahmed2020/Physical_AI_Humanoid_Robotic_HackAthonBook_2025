from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.progress import LearningProgress as ProgressModel
from ..models.progress_pydantic import LearningProgressCreate, LearningProgressUpdate


class ProgressService:
    @staticmethod
    def get_progress_by_id(db: Session, progress_id: int) -> Optional[ProgressModel]:
        return db.query(ProgressModel).filter(ProgressModel.id == progress_id).first()

    @staticmethod
    def get_progress_by_user_and_chapter(db: Session, user_id: int, chapter_id: int) -> Optional[ProgressModel]:
        return db.query(ProgressModel).filter(
            ProgressModel.user_id == user_id,
            ProgressModel.chapter_id == chapter_id
        ).first()

    @staticmethod
    def get_progress_by_user(db: Session, user_id: int) -> List[ProgressModel]:
        return db.query(ProgressModel).filter(ProgressModel.user_id == user_id).all()

    @staticmethod
    def get_progress_by_chapter(db: Session, chapter_id: int) -> List[ProgressModel]:
        return db.query(ProgressModel).filter(ProgressModel.chapter_id == chapter_id).all()

    @staticmethod
    def get_all_progress(db: Session, skip: int = 0, limit: int = 100) -> List[ProgressModel]:
        return db.query(ProgressModel).offset(skip).limit(limit).all()

    @staticmethod
    def create_progress(db: Session, progress: LearningProgressCreate) -> ProgressModel:
        # Check if progress already exists for this user and chapter
        existing_progress = db.query(ProgressModel).filter(
            ProgressModel.user_id == progress.user_id,
            ProgressModel.chapter_id == progress.chapter_id
        ).first()
        
        if existing_progress:
            # Update existing progress instead of creating a new one
            return ProgressService.update_progress(
                db, 
                existing_progress.id, 
                LearningProgressUpdate(
                    status=progress.status,
                    completion_percentage=progress.completion_percentage,
                    time_spent=progress.time_spent,
                    assessment_scores=progress.assessment_scores,
                    simulation_attempts=progress.simulation_attempts
                )
            )
        
        db_progress = ProgressModel(
            user_id=progress.user_id,
            chapter_id=progress.chapter_id,
            status=progress.status,
            completion_percentage=progress.completion_percentage,
            time_spent=progress.time_spent,
            assessment_scores=progress.assessment_scores,
            simulation_attempts=progress.simulation_attempts
        )
        
        db.add(db_progress)
        db.commit()
        db.refresh(db_progress)
        
        return db_progress

    @staticmethod
    def update_progress(db: Session, progress_id: int, progress_update: LearningProgressUpdate) -> Optional[ProgressModel]:
        db_progress = db.query(ProgressModel).filter(ProgressModel.id == progress_id).first()
        
        if not db_progress:
            return None

        # Update fields if provided
        if progress_update.status:
            db_progress.status = progress_update.status
        if progress_update.completion_percentage is not None:
            db_progress.completion_percentage = progress_update.completion_percentage
        if progress_update.time_spent is not None:
            db_progress.time_spent = progress_update.time_spent
        if progress_update.assessment_scores is not None:
            db_progress.assessment_scores = progress_update.assessment_scores
        if progress_update.simulation_attempts is not None:
            db_progress.simulation_attempts = progress_update.simulation_attempts

        # Update last_accessed
        db_progress.last_accessed = func.now()
        
        db.commit()
        db.refresh(db_progress)
        
        return db_progress

    @staticmethod
    def delete_progress(db: Session, progress_id: int) -> bool:
        db_progress = db.query(ProgressModel).filter(ProgressModel.id == progress_id).first()
        
        if not db_progress:
            return False

        db.delete(db_progress)
        db.commit()
        
        return True

    @staticmethod
    def get_user_progress_summary(db: Session, user_id: int):
        """Get a summary of user's progress across all chapters"""
        progress_records = db.query(ProgressModel).filter(ProgressModel.user_id == user_id).all()
        
        total_chapters = len(progress_records)
        completed_chapters = len([p for p in progress_records if p.status == "COMPLETED"])
        in_progress_chapters = len([p for p in progress_records if p.status == "IN_PROGRESS"])
        progress_percent = (completed_chapters / total_chapters * 100) if total_chapters > 0 else 0
        time_spent_total = sum(p.time_spent or 0 for p in progress_records)
        
        return {
            "total_chapters": total_chapters,
            "completed_chapters": completed_chapters,
            "in_progress_chapters": in_progress_chapters,
            "progress_percent": progress_percent,
            "time_spent_total": time_spent_total,
            "chapters": [
                {
                    "chapter_id": p.chapter_id,
                    "chapter_title": p.chapter.title if p.chapter else "Unknown Chapter",
                    "status": p.status,
                    "completion_percentage": p.completion_percentage,
                    "time_spent": p.time_spent,
                    "last_accessed": p.last_accessed,
                    "assessment_scores": p.assessment_scores
                }
                for p in progress_records
            ]
        }
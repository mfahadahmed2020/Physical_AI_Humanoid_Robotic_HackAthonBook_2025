from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database.database import get_db
from ...models.progress_pydantic import LearningProgress, LearningProgressCreate, LearningProgressUpdate
from ...services.progress_service import ProgressService
from ...auth.auth import get_current_active_user
from ...utils.error_handling import log_api_call
from ...utils.logging import app_logger


router = APIRouter()


@router.get("/", response_model=dict)
async def get_user_progress(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Retrieve the current user's learning progress across all chapters.
    """
    # Log the API call
    log_api_call(
        endpoint="/api/v1/progress",
        method="GET",
        user_id=current_user.id if current_user else None
    )
    
    # Get user progress summary from the service
    progress_summary = ProgressService.get_user_progress_summary(db, current_user.id)
    
    # Log successful retrieval
    app_logger.info(
        f"Retrieved progress for user {current_user.id}", 
        extra={"user_id": current_user.id, "total_chapters": progress_summary["total_chapters"]}
    )
    
    return progress_summary


@router.post("/{chapter_id}")
async def update_progress(
    chapter_id: int,
    progress_update: LearningProgressUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Update progress for a specific chapter.
    """
    # Log the API call
    log_api_call(
        endpoint=f"/api/v1/progress/{chapter_id}",
        method="POST",
        user_id=current_user.id if current_user else None,
        extra={"chapter_id": chapter_id, "progress_update": progress_update.dict()}
    )
    
    # First, check if there's existing progress for this user and chapter
    existing_progress = ProgressService.get_progress_by_user_and_chapter(db, current_user.id, chapter_id)
    
    if existing_progress:
        # Update existing progress
        updated_progress = ProgressService.update_progress(db, existing_progress.id, progress_update)
        if not updated_progress:
            app_logger.error(f"Failed to update progress for user {current_user.id} and chapter {chapter_id}", 
                           extra={"user_id": current_user.id, "chapter_id": chapter_id})
            raise HTTPException(status_code=400, detail="Failed to update progress")
    else:
        # Create new progress record
        progress_create = LearningProgressCreate(
            user_id=current_user.id,
            chapter_id=chapter_id,
            status=progress_update.status,
            completion_percentage=progress_update.completion_percentage,
            time_spent=progress_update.time_spent,
            assessment_scores=progress_update.assessment_scores,
            simulation_attempts=progress_update.simulation_attempts
        )
        updated_progress = ProgressService.create_progress(db, progress_create)
        if not updated_progress:
            app_logger.error(f"Failed to create progress for user {current_user.id} and chapter {chapter_id}", 
                           extra={"user_id": current_user.id, "chapter_id": chapter_id})
            raise HTTPException(status_code=400, detail="Failed to create progress")
    
    # Log successful update
    app_logger.info(
        f"Updated progress for user {current_user.id} and chapter {chapter_id}", 
        extra={"user_id": current_user.id, "chapter_id": chapter_id, "status": progress_update.status}
    )
    
    return updated_progress
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database.database import get_db
from ...models.assessment_pydantic import Assessment, AssessmentCreate, AssessmentSubmission, AssessmentSubmissionCreate, SubmissionResult
from ...services.assessment_service import AssessmentService
from ...auth.auth import get_current_active_user
from ...utils.error_handling import log_api_call
from ...utils.logging import app_logger


router = APIRouter()


@router.get("/{chapter_id}/assessments", response_model=List[Assessment])
async def get_assessments_for_chapter(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Get assessments for a specific chapter.
    """
    # Log the API call
    log_api_call(
        endpoint=f"/api/v1/chapters/{chapter_id}/assessments",
        method="GET",
        user_id=current_user.id if current_user else None,
        extra={"chapter_id": chapter_id}
    )
    
    # Get assessments from the service
    assessments = AssessmentService.get_assessments_by_chapter(db, chapter_id)
    
    # Log successful retrieval
    app_logger.info(
        f"Retrieved {len(assessments)} assessments for chapter {chapter_id}", 
        extra={"user_id": current_user.id, "chapter_id": chapter_id, "count": len(assessments)}
    )
    
    return assessments


@router.get("/assessments/{assessment_id}", response_model=Assessment)
async def get_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Get details of a specific assessment.
    """
    # Log the API call
    log_api_call(
        endpoint=f"/api/v1/assessments/{assessment_id}",
        method="GET",
        user_id=current_user.id if current_user else None,
        extra={"assessment_id": assessment_id}
    )
    
    # Get the assessment from the service
    assessment = AssessmentService.get_assessment_by_id(db, assessment_id)
    
    if not assessment:
        app_logger.error(f"Assessment with ID {assessment_id} not found", 
                        extra={"user_id": current_user.id, "assessment_id": assessment_id})
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Log successful retrieval
    app_logger.info(
        f"Retrieved assessment {assessment_id}", 
        extra={"user_id": current_user.id, "assessment_id": assessment_id}
    )
    
    return assessment


@router.post("/assessments/{assessment_id}/submit", response_model=SubmissionResult)
async def submit_assessment(
    assessment_id: int,
    submission: AssessmentSubmissionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Submit answers for an assessment.
    """
    # Log the API call
    log_api_call(
        endpoint=f"/api/v1/assessments/{assessment_id}/submit",
        method="POST",
        user_id=current_user.id if current_user else None,
        extra={"assessment_id": assessment_id, "user_id": current_user.id}
    )
    
    # Ensure the submission is for the current user
    submission.user_id = current_user.id
    
    # Create the submission through the service
    db_submission = AssessmentService.create_assessment_submission(db, submission)
    
    if not db_submission:
        app_logger.error(f"Failed to create submission for assessment {assessment_id} by user {current_user.id}",
                        extra={"assessment_id": assessment_id, "user_id": current_user.id})
        raise HTTPException(status_code=400, detail="Failed to submit assessment")
    
    # For now, we'll return the submission as is without grading
    # In a real implementation, you'd have more sophisticated grading logic
    result = SubmissionResult(
        id=db_submission.id,
        assessment_id=db_submission.assessment_id,
        user_id=db_submission.user_id,
        answers=db_submission.answers,
        score=db_submission.score or 0,
        max_score=db_submission.assessment.max_score,
        percentage=(db_submission.score or 0) / db_submission.assessment.max_score * 100 if db_submission.assessment.max_score > 0 else 0,
        status=db_submission.status,
        graded_at=db_submission.graded_at,
        feedback=db_submission.feedback,
        created_at=db_submission.created_at,
        updated_at=db_submission.updated_at
    )
    
    # Log successful submission
    app_logger.info(
        f"Submitted assessment {assessment_id} by user {current_user.id}", 
        extra={"user_id": current_user.id, "assessment_id": assessment_id}
    )
    
    return result
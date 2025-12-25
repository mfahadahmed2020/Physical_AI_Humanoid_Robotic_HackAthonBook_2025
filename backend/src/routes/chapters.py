from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database.database import get_db
from ...models.chapter_pydantic import TextbookChapter, TextbookChapterCreate
from ...services.chapter_service import ChapterService
from ...auth.auth import get_current_active_user
from ...utils.error_handling import log_api_call
from ...utils.logging import app_logger


router = APIRouter()


@router.get("/", response_model=List[TextbookChapter])
async def get_chapters(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=50),
    level: Optional[str] = Query(None),
    topic_area: Optional[str] = Query(None),
    current_user = Depends(get_current_active_user)
):
    """
    Retrieve a list of textbook chapters with optional filtering and pagination.
    """
    # Log the API call
    log_api_call(
        endpoint="/api/v1/chapters",
        method="GET", 
        user_id=current_user.id if current_user else None,
        extra={"skip": skip, "limit": limit, "level": level, "topic_area": topic_area}
    )
    
    # Get chapters from the service
    chapters = ChapterService.get_chapters(db, skip=skip, limit=limit, level=level, topic_area=topic_area)
    
    # Log successful retrieval
    app_logger.info(
        f"Retrieved {len(chapters)} chapters", 
        extra={"user_id": current_user.id, "count": len(chapters)}
    )
    
    # Calculate total for pagination info
    total = ChapterService.get_chapters_count(db)
    
    # For the API response, we'll return the chapters with total count
    # Note: In a real implementation, you'd probably want to return pagination metadata
    return chapters


@router.get("/{slug}", response_model=TextbookChapter)
async def get_chapter_by_slug(
    slug: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Retrieve a specific textbook chapter by slug.
    """
    # Log the API call
    log_api_call(
        endpoint=f"/api/v1/chapters/{slug}",
        method="GET",
        user_id=current_user.id if current_user else None,
        extra={"slug": slug}
    )

    # Get the chapter from the service
    chapter = ChapterService.get_chapter_by_slug(db, slug)

    if not chapter:
        app_logger.error(f"Chapter with slug {slug} not found", extra={"user_id": current_user.id})
        raise HTTPException(status_code=404, detail="Chapter not found")

    # Log successful retrieval
    app_logger.info(
        f"Retrieved chapter {slug}",
        extra={"user_id": current_user.id, "slug": slug}
    )

    return chapter
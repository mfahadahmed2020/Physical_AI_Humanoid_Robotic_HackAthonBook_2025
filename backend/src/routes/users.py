from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User as UserModel
from ..models.user_pydantic import User, UserCreate, UserUpdate
from ..services.user_service import UserService
from ..auth.auth import get_current_active_user
from ..utils.error_handling import log_api_call
from ..utils.logging import app_logger

router = APIRouter()


@router.get("/profile", response_model=User)
def get_current_user_profile(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve the current user's profile information.
    """
    # Log the API call
    log_api_call(
        endpoint="/api/v1/users/profile",
        method="GET",
        user_id=current_user.id if current_user else None
    )

    # Fetch the user from the database
    user = UserService.get_user_by_id(db, current_user.id)

    if not user:
        app_logger.error(f"User with ID {current_user.id} not found in database",
                        extra={"user_id": current_user.id})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Log successful retrieval
    app_logger.info(f"Retrieved profile for user {current_user.id}",
                   extra={"user_id": current_user.id})

    return user


@router.put("/profile", response_model=User)
def update_current_user_profile(
    user_update: UserUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update the current user's profile information.
    """
    # Log the API call
    log_api_call(
        endpoint="/api/v1/users/profile",
        method="PUT",
        user_id=current_user.id if current_user else None,
        extra={"update_data": user_update.dict(exclude_unset=True)}
    )

    # Update the user through the service
    updated_user = UserService.update_user(db, current_user.id, user_update)

    if not updated_user:
        app_logger.error(f"Failed to update user profile for ID {current_user.id}",
                        extra={"user_id": current_user.id})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update user profile"
        )

    # Log successful update
    app_logger.info(f"Updated profile for user {current_user.id}",
                   extra={"user_id": current_user.id})

    return updated_user


@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific user by ID.
    Note: In a real implementation, you might want to restrict access based on user roles.
    """
    # Log the API call
    log_api_call(
        endpoint=f"/api/v1/users/{user_id}",
        method="GET",
        user_id=current_user.id if current_user else None,
        extra={"target_user_id": user_id}
    )

    db_user = UserService.get_user_by_id(db, user_id)
    if not db_user:
        app_logger.error(f"User with ID {user_id} not found",
                        extra={"requesting_user_id": current_user.id, "target_user_id": user_id})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Log successful retrieval
    app_logger.info(f"Retrieved user {user_id} by user {current_user.id}",
                   extra={"requesting_user_id": current_user.id, "target_user_id": user_id})

    return db_user


@router.get("/", response_model=List[User])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of all users (with pagination).
    Note: In a real implementation, you might want to restrict access based on user roles.
    """
    # Log the API call
    log_api_call(
        endpoint="/api/v1/users/",
        method="GET",
        user_id=current_user.id if current_user else None,
        extra={"skip": skip, "limit": limit}
    )

    users = UserService.get_users(db, skip=skip, limit=limit)

    # Log successful retrieval
    app_logger.info(f"Retrieved {len(users)} users by user {current_user.id}",
                   extra={"requesting_user_id": current_user.id, "count": len(users)})

    return users


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_new_user(
    user: UserCreate,
    current_user = Depends(get_current_active_user),  # In a real app, you might allow registration without auth
    db: Session = Depends(get_db)
):
    """
    Create a new user.
    Note: In a real implementation, registration might be allowed without authentication.
    """
    # Log the API call
    log_api_call(
        endpoint="/api/v1/users/",
        method="POST",
        user_id=current_user.id if current_user else None,
        extra={"new_user_email": user.email, "new_user_username": user.username}
    )

    # Check if user with this email already exists
    existing_user = UserService.get_user_by_email(db, user.email)
    if existing_user:
        app_logger.warning(f"Attempt to create user with existing email: {user.email}",
                         extra={"requesting_user_id": current_user.id, "email": user.email})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if user with this username already exists
    existing_username = UserService.get_user_by_username(db, user.username)
    if existing_username:
        app_logger.warning(f"Attempt to create user with existing username: {user.username}",
                         extra={"requesting_user_id": current_user.id, "username": user.username})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    db_user = UserService.create_user(db, user)

    # Log successful creation
    app_logger.info(f"Created new user with ID {db_user.id}",
                   extra={"requesting_user_id": current_user.id, "new_user_id": db_user.id})

    return db_user


@router.put("/{user_id}", response_model=User)
def update_existing_user(
    user_id: int,
    user_update: UserUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing user.
    Note: In a real implementation, you might restrict this to admin users or the user themselves.
    """
    # Log the API call
    log_api_call(
        endpoint=f"/api/v1/users/{user_id}",
        method="PUT",
        user_id=current_user.id if current_user else None,
        extra={"target_user_id": user_id, "update_data": user_update.dict(exclude_unset=True)}
    )

    db_user = UserService.update_user(db, user_id, user_update)
    if not db_user:
        app_logger.error(f"Failed to update user with ID {user_id}",
                        extra={"requesting_user_id": current_user.id, "target_user_id": user_id})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Log successful update
    app_logger.info(f"Updated user {user_id} by user {current_user.id}",
                   extra={"requesting_user_id": current_user.id, "target_user_id": user_id})

    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_user(
    user_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete an existing user.
    Note: In a real implementation, you might restrict this to admin users.
    """
    # Log the API call
    log_api_call(
        endpoint=f"/api/v1/users/{user_id}",
        method="DELETE",
        user_id=current_user.id if current_user else None,
        extra={"target_user_id": user_id}
    )

    success = UserService.delete_user(db, user_id)
    if not success:
        app_logger.error(f"Failed to delete user with ID {user_id}",
                        extra={"requesting_user_id": current_user.id, "target_user_id": user_id})
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Log successful deletion
    app_logger.info(f"Deleted user {user_id} by user {current_user.id}",
                   extra={"requesting_user_id": current_user.id, "target_user_id": user_id})

    return
from typing import Optional
from sqlalchemy.orm import Session
from ..models.user import User as UserModel
from ..models.user_pydantic import UserCreate, UserUpdate, UserInDB
from ..auth.auth import get_password_hash


class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.email == email).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.username == username).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(UserModel).offset(skip).limit(limit).all()

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> UserModel:
        # Hash the password before storing
        hashed_password = get_password_hash(user.password)
        
        # Create the user object
        db_user = UserModel(
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role.value if hasattr(user.role, 'value') else user.role,
            hashed_password=hashed_password
        )
        
        # Add to database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[UserModel]:
        db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        
        if not db_user:
            return None

        # Update fields if provided
        if user_update.email:
            db_user.email = user_update.email
        if user_update.username:
            db_user.username = user_update.username
        if user_update.first_name is not None:
            db_user.first_name = user_update.first_name
        if user_update.last_name is not None:
            db_user.last_name = user_update.last_name
        if user_update.role:
            db_user.role = user_update.role.value if hasattr(user_update.role, 'value') else user_update.role
        if user_update.is_active is not None:
            db_user.is_active = user_update.is_active
        if user_update.password:
            db_user.hashed_password = get_password_hash(user_update.password)
        
        db.commit()
        db.refresh(db_user)
        
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        
        if not db_user:
            return False

        db.delete(db_user)
        db.commit()
        
        return True

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[UserModel]:
        from ..auth.auth import verify_password
        
        user = db.query(UserModel).filter(UserModel.username == username).first()
        
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        return user
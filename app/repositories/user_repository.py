# app/repositories/user_repository.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

class UserRepository:
    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(db: Session, user_in: UserCreate):
        hashed_pwd = get_password_hash(user_in.password)
        db_user = User(
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=hashed_pwd,
            is_active=True,
            is_superuser=False
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update_password(db: Session, user: User, new_password: str):
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        db.refresh(user)
        return user
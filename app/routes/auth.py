from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.user import UserCreate, UserLogin
from app.services import auth as auth_service 


router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user = auth_service.register_user(user_data, db)
    return {
        "message": f"User {user.username} Registered Successfully"
    }

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    token = auth_service.login_user(db, username=user_data.username, password=user_data.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {
        "access_token": token, "token_type": "bearer"
    }


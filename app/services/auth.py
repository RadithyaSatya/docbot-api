from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError
from sqlalchemy.orm import Session
from app.core.security import create_access_token, decode_token, hash_password, verify_password
from app.db import get_db
from app.models.user import User
from app.repositories import user_repo


oauth2_scheme = HTTPBearer()

def register_user(user_data, db):
    if user_repo.get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    if user_repo.get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Email lready taken"
        )
    
    hashed = hash_password(user_data.password)
    new_user = User(
        username = user_data.username,
        email = user_data.email,
        password_hash = hashed
    )
    user_repo.create_user(db, new_user)
    return new_user

def login_user(db: Session, username: str, password:str):
    user :User = user_repo.get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return create_access_token({"sub":str(user.id)})

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token is invalid",
        headers={"WWW-Authenticate":"Bearer"},
    )

    try:
        token = credentials.credentials
        payload = decode_token(token)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credential_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (JWTError, ValueError) as e:
        print("❌ JWTError:", str(e))
        raise credential_exception
    
    user = user_repo.get_user_by_id(db, user_id)
    if user is None:
        raise credential_exception
    return user
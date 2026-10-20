# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

# Tunatumia argon2 kama mpango mkuu wa hash ya nywila
password_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return password_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Kutengeneza token maalum ya kubadilisha nenosiri (inaisha baada ya dakika 15)
def create_password_reset_token(email: str) -> str:
    delta = timedelta(minutes=15)
    expire = datetime.now() + delta
    to_encode = {"sub": email, "type": "reset_password", "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Kukagua na kusoma tokeni ya kubadilisha nenosiri
def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "reset_password":
            return None
        return payload.get("sub")
    except JWTError:
        return None
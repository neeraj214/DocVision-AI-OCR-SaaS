from __future__ import annotations
from datetime import datetime, timedelta
from typing import Any, Dict
from jose import jwt
from passlib.context import CryptContext
from backend.app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: str, role: str = "user", expires_minutes: int | None = None) -> Dict[str, Any]:
    expire_delta = timedelta(minutes=expires_minutes or settings.access_token_expire_minutes)
    expire = datetime.utcnow() + expire_delta
    payload = {"sub": subject, "exp": int(expire.timestamp()), "role": role}
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)
    return {"access_token": token, "expires_in": int(expire_delta.total_seconds())}


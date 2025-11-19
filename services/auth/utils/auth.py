from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import os
from jose import jwt
import bcrypt


def _truncate_password(password: str) -> bytes:
    pw_bytes = password.encode("utf-8")
    if len(pw_bytes) > 72:
        pw_bytes = pw_bytes[:72]
    return pw_bytes


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pw = _truncate_password(plain_password)
    try:
        return bcrypt.checkpw(pw, hashed_password.encode("utf-8"))
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    pw = _truncate_password(password)
    hashed = bcrypt.hashpw(pw, bcrypt.gensalt())
    return hashed.decode("utf-8")

def create_access_token(data: Dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=int(os.getenv("AUTH_ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    )
    to_encode.update({"exp": expire})
    secret = os.getenv("AUTH_SECRET_KEY", "not-secure-local-dev")
    algorithm = os.getenv("AUTH_ALGORITHM", "HS256")
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=algorithm)
    return encoded_jwt

def create_refresh_token(data: Dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        days=int(os.getenv("AUTH_REFRESH_TOKEN_EXPIRE_DAYS", 7))
    )
    to_encode.update({"exp": expire})
    secret = os.getenv("AUTH_SECRET_KEY", "not-secure-local-dev")
    algorithm = os.getenv("AUTH_ALGORITHM", "HS256")
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=algorithm)
    return encoded_jwt
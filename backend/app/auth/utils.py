"""Password hashing and JWT utilities."""

import hashlib
import uuid
from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerifyMismatchError

from app.core.config import get_settings

hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Hash password with Argon2id."""
    return hasher.hash(password)


def verify_password(password: str, hash_: str) -> bool:
    """Verify password against hash. Return False on error."""
    try:
        hasher.verify(hash_, password)
        return True
    except (VerifyMismatchError, InvalidHash):
        return False


def create_access_token(user_id: str, role: str, expires_in_minutes: int | None = None) -> str:
    """Create JWT access token."""
    settings = get_settings()
    if expires_in_minutes is None:
        expires_in_minutes = settings.jwt_access_ttl_minutes

    payload = {
        "sub": user_id,
        "role": role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes),
        "type": "access",
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def create_refresh_token(user_id: str) -> tuple[str, str]:
    """Create refresh token and its hash. Return (token, hash)."""
    settings = get_settings()

    token = jwt.encode(
        {
            "sub": user_id,
            "jti": str(uuid.uuid4()),
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(days=settings.refresh_ttl_days),
            "type": "refresh",
        },
        settings.jwt_secret,
        algorithm="HS256",
    )
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    return token, token_hash


def verify_token(token: str, token_type: str = "access") -> dict | None:
    """Verify and decode token. Return payload on success, None on failure."""
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        if payload.get("type") != token_type:
            return None
        return payload
    except jwt.InvalidTokenError:
        return None

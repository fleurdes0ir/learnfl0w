"""Auth service layer."""

import hashlib
from datetime import datetime, timezone

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import create_access_token, create_refresh_token, hash_password, verify_password
from app.core.config import get_settings
from app.models.user import RefreshToken, User


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.settings = get_settings()

    async def register(
        self, email: str, password: str
    ) -> tuple[User, str, str]:
        """Register new user and return (user, access_token, refresh_token)."""
        from datetime import timedelta

        # Check if email exists
        result = await self.session.execute(select(User).where(User.email == email.lower()))
        if result.scalar_one_or_none():
            raise ValueError("Email already registered")

        # Determine role from ADMIN_EMAILS
        role = "student"
        if email.lower() in [
            e.strip().lower() for e in self.settings.admin_emails.split(",") if e.strip()
        ]:
            role = "admin"

        # Create user
        user = User(
            email=email.lower(),
            password_hash=hash_password(password),
            role=role,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        # Create tokens
        access_token = create_access_token(str(user.id), user.role)
        refresh_token, token_hash = create_refresh_token(str(user.id))

        # Store refresh token
        rt = RefreshToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=datetime.now(timezone.utc) + timedelta(days=self.settings.refresh_ttl_days),
        )
        self.session.add(rt)
        await self.session.commit()

        return user, access_token, refresh_token

    async def login(self, email: str, password: str) -> tuple[User, str, str]:
        """Login and return (user, access_token, refresh_token)."""
        from datetime import timedelta

        result = await self.session.execute(select(User).where(User.email == email.lower()))
        user = result.scalar_one_or_none()

        if not user or not user.is_active or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        # Create tokens
        access_token = create_access_token(str(user.id), user.role)
        refresh_token, token_hash = create_refresh_token(str(user.id))

        # Store refresh token
        rt = RefreshToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=datetime.now(timezone.utc) + timedelta(days=self.settings.refresh_ttl_days),
        )
        self.session.add(rt)
        await self.session.commit()

        return user, access_token, refresh_token

    async def refresh(self, refresh_token: str) -> tuple[str, str]:
        """Rotate refresh token. Return (new_access_token, new_refresh_token)."""
        from datetime import timedelta

        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()

        # Find token
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        rt = result.scalar_one_or_none()

        if not rt or rt.revoked_at or rt.expires_at < datetime.now(timezone.utc):
            raise ValueError("Invalid or expired refresh token")

        # Revoke old token
        rt.revoked_at = datetime.now(timezone.utc)

        # Check for reuse (security: revoke all user tokens)
        result = await self.session.execute(
            select(RefreshToken)
            .where(RefreshToken.user_id == rt.user_id)
            .where(RefreshToken.revoked_at.is_(None))
            .where(RefreshToken.id != rt.id)
        )
        if result.scalar_one_or_none():
            # Token reuse detected - revoke all user tokens
            await self.session.execute(
                update(RefreshToken)
                .where(RefreshToken.user_id == rt.user_id)
                .values(revoked_at=datetime.now(timezone.utc))
            )
            await self.session.commit()
            raise ValueError("Token reuse detected. All sessions revoked.")

        # Get user
        result = await self.session.execute(select(User).where(User.id == rt.user_id))
        user = result.scalar_one_or_none()
        if not user or not user.is_active:
            raise ValueError("User not found or inactive")

        # Create new tokens
        access_token = create_access_token(str(user.id), user.role)
        new_refresh_token, new_token_hash = create_refresh_token(str(user.id))

        new_rt = RefreshToken(
            user_id=user.id,
            token_hash=new_token_hash,
            expires_at=datetime.now(timezone.utc) + timedelta(days=self.settings.refresh_ttl_days),
        )
        self.session.add(new_rt)
        await self.session.commit()

        return access_token, new_refresh_token

    async def logout(self, refresh_token: str) -> None:
        """Revoke refresh token."""
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        await self.session.execute(
            update(RefreshToken)
            .where(RefreshToken.token_hash == token_hash)
            .values(revoked_at=datetime.now(timezone.utc))
        )
        await self.session.commit()

    async def delete_account(self, user_id: str) -> None:
        """Delete user account and all related data."""
        await self.session.execute(delete(User).where(User.id == user_id))
        await self.session.commit()

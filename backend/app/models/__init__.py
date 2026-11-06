"""SQLAlchemy models. Import all models here for Alembic discovery."""

from app.models.ai import AiRun
from app.models.catalog import (
    CareerPath,
    Certification,
    Course,
    CourseCareerpathMap,
    LearningMaterial,
)
from app.models.conversation import Conversation, Message
from app.models.user import RefreshToken, User

__all__ = [
    "User",
    "RefreshToken",
    "AiRun",
    "Course",
    "CareerPath",
    "CourseCareerpathMap",
    "Certification",
    "LearningMaterial",
    "Conversation",
    "Message",
]

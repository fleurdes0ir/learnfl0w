"""Aggregates all v1 routers. Add routers here as specs are implemented."""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.catalog import router as catalog_router

api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(auth_router)
api_v1.include_router(catalog_router)

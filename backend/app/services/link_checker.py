"""Link checker service: verify certification and material URLs."""

import asyncio
import logging
from datetime import date

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.catalog import Certification, LearningMaterial

logger = logging.getLogger(__name__)


class LinkChecker:
    """Check URLs for certifications and learning materials."""

    def __init__(
        self,
        db: AsyncSession,
        timeout: float = 10.0,
        max_concurrent: int = 5,
        verify_days: int = 90,
    ):
        self.db = db
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        self.verify_days = verify_days
        self.checked = 0
        self.failed = 0
        self.marked_review = 0

    async def check_url(self, url: str) -> bool:
        """Check if URL is accessible (HEAD or GET)."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Try HEAD first (faster)
                resp = await client.head(url, follow_redirects=True)
                if resp.status_code < 400:
                    return True
                # Fallback to GET if HEAD not allowed
                resp = await client.get(url, follow_redirects=True)
                return resp.status_code < 400
            except Exception as e:
                logger.debug(f"URL check failed: {url} - {e}")
                return False

    async def check_certification(self, cert: Certification) -> None:
        """Check certification URL and update status."""
        self.checked += 1
        is_ok = await self.check_url(cert.url)
        today = date.today()

        if not is_ok:
            logger.warning(f"Certification {cert.code} URL dead: {cert.url}")
            cert.status = "needs_review"
            self.failed += 1
            self.marked_review += 1
        elif (
            cert.last_verified_at is None
            or (  # noqa: E501
                today - cert.last_verified_at
            ).days
            > self.verify_days
        ):
            cert.status = "needs_review"
            self.marked_review += 1

        cert.last_verified_at = today

    async def check_material(self, material: LearningMaterial) -> None:
        """Check material URL and update status."""
        self.checked += 1
        is_ok = await self.check_url(material.url)
        today = date.today()

        if not is_ok:
            logger.warning(f"Material {material.code} URL dead: {material.url}")
            material.status = "needs_review"
            self.failed += 1
            self.marked_review += 1
        elif (
            material.last_verified_at is None
            or (  # noqa: E501
                today - material.last_verified_at
            ).days
            > self.verify_days
        ):
            material.status = "needs_review"
            self.marked_review += 1

        material.last_verified_at = today

    async def run(self) -> dict[str, int]:
        """Check all certifications and materials with active status."""
        logger.info("Starting link check...")

        # Get active certifications and materials
        certs_result = await self.db.execute(
            select(Certification).where(Certification.status.in_(["active", "needs_review"]))
        )
        certs = list(certs_result.scalars().all())

        materials_result = await self.db.execute(
            select(LearningMaterial).where(LearningMaterial.status.in_(["active", "needs_review"]))
        )
        materials = list(materials_result.scalars().all())

        logger.info(f"Checking {len(certs)} certifications and {len(materials)} materials")

        # Check with concurrency limit
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def check_cert_with_limit(cert: Certification) -> None:
            async with semaphore:
                await self.check_certification(cert)

        async def check_material_with_limit(material: LearningMaterial) -> None:
            async with semaphore:
                await self.check_material(material)

        # Run all checks
        tasks = [check_cert_with_limit(c) for c in certs] + [
            check_material_with_limit(m) for m in materials
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

        await self.db.commit()

        logger.info(
            f"Link check complete: {self.checked} checked, {self.failed} failed, "
            f"{self.marked_review} marked for review"
        )

        return {
            "checked": self.checked,
            "failed": self.failed,
            "marked_review": self.marked_review,
        }

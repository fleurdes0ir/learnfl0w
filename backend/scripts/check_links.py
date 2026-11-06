"""Link checker CLI: verify all catalog URLs and mark dead links.

Run: python scripts/check_links.py
"""

import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.services.link_checker import LinkChecker

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


async def main() -> None:
    """Run link checker."""
    settings = get_settings()
    engine = create_async_engine(settings.database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        checker = LinkChecker(session, timeout=10.0, max_concurrent=5, verify_days=90)
        result = await checker.run()

    logger.info(f"✅ Link check done: {result}")


if __name__ == "__main__":
    asyncio.run(main())

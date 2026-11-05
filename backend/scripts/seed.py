"""Load catalog seed data from data/seed into database (idempoten).

Upsert: jika `code` ada, skip; jika baru, insert.
Mencegah duplikasi saat `make seed` dijalankan berulang.
"""

import asyncio
import csv
import json
import uuid
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.models.catalog import CareerPath, Course, CourseCareerpathMap


async def load_seed() -> None:
    """Load courses, career paths, and mappings idempotently."""
    settings = get_settings()
    seed_dir = Path(settings.seed_dir)

    # Baca file seed
    courses_data = list(csv.DictReader((seed_dir / "courses.csv").open(encoding="utf-8")))
    mapping_data = list(csv.DictReader((seed_dir / "course_career_map.csv").open(encoding="utf-8")))
    paths_list = json.loads((seed_dir / "career_paths.json").read_text(encoding="utf-8"))

    # Setup DB
    engine = create_async_engine(settings.database_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Load career paths (harus duluan karena FK)
        cp_map: dict[str, uuid.UUID] = {}
        for path_data in paths_list:
            path_code = path_data["code"]
            result = await session.execute(select(CareerPath).where(CareerPath.code == path_code))
            existing = result.scalars().one_or_none()

            if existing:
                cp_map[path_code] = existing.id
                print(f"  CareerPath {path_code} exists (skip)")
            else:
                new_path = CareerPath(
                    id=uuid.uuid4(),
                    code=path_code,
                    name=path_data.get("name", path_code),
                    description=path_data.get("description", ""),
                    template_stages=path_data.get("template_stages", {}),
                    is_active=True,
                )
                session.add(new_path)
                cp_map[path_code] = new_path.id
                print(f"  CareerPath {path_code} inserted")

        await session.flush()

        # Load courses
        course_map: dict[str, uuid.UUID] = {}
        for course in courses_data:
            result = await session.execute(select(Course).where(Course.code == course["code"]))
            existing = result.scalars().one_or_none()

            if existing:
                course_map[course["code"]] = existing.id
                print(f"  Course {course['code']} exists (skip)")
            else:
                new_course = Course(
                    id=uuid.uuid4(),
                    code=course["code"],
                    name=course["name"],
                    semester=int(course["semester"]),
                    description=course["description"],
                    is_mappable=course.get("is_mappable", "true").lower() == "true",
                )
                session.add(new_course)
                course_map[course["code"]] = new_course.id
                print(f"  Course {course['code']} inserted")

        await session.flush()

        # Load mappings (course → career path)
        for mapping in mapping_data:
            course_code = mapping["course_code"]
            path_code = mapping["career_path_code"]
            relevance = int(mapping.get("relevance", 1))

            course_id = course_map.get(course_code)
            path_id = cp_map.get(path_code)

            if not course_id or not path_id:
                print(f"  Mapping {course_code} → {path_code} skipped (missing ref)")
                continue

            result = await session.execute(
                select(CourseCareerpathMap).where(
                    (CourseCareerpathMap.course_id == course_id)
                    & (CourseCareerpathMap.career_path_id == path_id)
                )
            )
            existing = result.scalars().one_or_none()

            if existing:
                print(f"  Mapping {course_code} → {path_code} exists (skip)")
            else:
                new_mapping = CourseCareerpathMap(
                    course_id=course_id, career_path_id=path_id, relevance=relevance
                )
                session.add(new_mapping)
                print(f"  Mapping {course_code} → {path_code} inserted")

        await session.commit()
        print(
            f"\n✅ Seed complete: {len(courses_data)} courses, "
            f"{len(paths_list)} paths, {len(mapping_data)} mappings"
        )


def main() -> None:
    asyncio.run(load_seed())


if __name__ == "__main__":
    main()

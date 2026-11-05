"""Load catalog seed data from data/seed into the database.

Skeleton: validates the seed files and prints counts.
SPEC-004 T-1: implement idempotent upserts into the catalog tables.
"""

import csv
import json
from pathlib import Path

from app.core.config import get_settings


def main() -> None:
    seed_dir = Path(get_settings().seed_dir)
    courses = list(csv.DictReader((seed_dir / "courses.csv").open(encoding="utf-8")))
    mapping = list(csv.DictReader((seed_dir / "course_career_map.csv").open(encoding="utf-8")))
    paths = json.loads((seed_dir / "career_paths.json").read_text(encoding="utf-8"))
    print(f"courses={len(courses)} mappings={len(mapping)} career_paths={len(paths)}")


if __name__ == "__main__":
    main()

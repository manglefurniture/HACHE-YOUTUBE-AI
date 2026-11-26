#!/usr/bin/env python3
"""Metadata preflight for fictional cast; not an image similarity detector."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "production/series/humanoid-robots-batch-a-drafts.json"


def normalized(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Missing visual identity field")
    return " ".join(value.casefold().split())


def validate(data):
    ids = set()
    seen = {}
    episodes = data["episodes"]
    if not episodes:
        raise ValueError("Empty episode list")

    def unique(field, value):
        value = normalized(value)
        bucket = seen.setdefault(field, set())
        if value in bucket:
            raise ValueError(f"Repeated {field}: {value}")
        bucket.add(value)

    for ep in episodes:
        eid = ep["id"]
        if not re.fullmatch(r"S\d{2,}", eid):
            raise ValueError("Invalid episode ID")
        if eid in ids:
            raise ValueError("Duplicate episode")
        ids.add(eid)
        identity = ep["visual_identity"]
        human, robot = identity["human"], identity["robot"]
        for item, suffix in ((human, "H01"), (robot, "R01")):
            if item["id"] != f"{eid}-{suffix}":
                raise ValueError("Identity ID does not match episode")
            unique("identity_id", item["id"])
        if type(human["age"]) is not int or not 18 <= human["age"] <= 120:
            raise ValueError("Invalid adult character age")
        for field in ("name", "face", "hair", "wardrobe"):
            unique(field, human[field])
        for field in ("role", "design"):
            unique(field, robot[field])
        for field in ("setting", "composition"):
            unique(field, identity[field])
        for field in ("reference_status", "historical_visual_review"):
            if identity[field] != "pending":
                raise ValueError("Metadata preflight cannot certify images or historical review")
    return len(episodes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT)
    args = parser.parse_args()
    try:
        count = validate(json.loads(args.manifest.read_text(encoding="utf-8")))
    except (OSError, KeyError, TypeError, AttributeError, ValueError) as exc:
        parser.exit(1, f"Visual metadata invalid: {exc}\n")
    print(f"OK: {count} distinct episode profiles; image generation readiness NOT certified")


if __name__ == "__main__":
    main()

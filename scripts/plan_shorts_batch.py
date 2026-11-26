#!/usr/bin/env python3
"""Read-only Shorts batch planner. No providers, network or publication."""
import argparse
import json
import re
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[1] / "production/series/humanoid-robots.json"
STAGES = ("research", "script", "narration", "storyboard", "visuals", "edit", "qa", "review", "publication")
PAID_OR_EXTERNAL = {"narration", "visuals", "publication"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(data):
    require(data["schema_version"] == 1, "Unsupported schema")
    episodes = data["episodes"]
    ids = [ep["id"] for ep in episodes]
    require(bool(ids) and all(re.fullmatch(r"S\d{2,}", i) for i in ids), "Invalid episode IDs")
    numbers = [int(i[1:]) for i in ids]
    require(numbers == list(range(numbers[0], numbers[-1] + 1)), "Episode IDs must be unique and consecutive")
    require(data["episode_range"] == [ids[0], ids[-1]], "Episode range mismatch")
    batches = data["batches"]
    require(bool(batches) and all(b["episode_ids"] for b in batches), "Empty batch")
    require(len({b["id"] for b in batches}) == len(batches), "Duplicate batch")
    require([i for b in batches for i in b["episode_ids"]] == ids, "Batches must partition episodes in order")
    research = data["research"]
    require(research["vidiq"] == "reuse_existing_only" and type(research["credit_budget"]) is int and research["credit_budget"] == 0, "New vidIQ spending blocked")
    sources = research["sources"]
    require(all(s["url"].startswith("https://") and s["scope"].strip() for s in sources.values()), "Invalid source")
    authorization = data["policy"]["authorization"]
    require(all(authorization[k] is False for k in ("paid_generation", "gpu_rental", "publication")), "This planner accepts only unapproved, no-spend manifests")
    for ep in episodes:
        require(ep["state"] == "planned", "Only planned episodes are supported")
        require(ep["research_verified"] is False, "This planner cannot certify research")
        require(all(isinstance(ep[k], str) and ep[k].strip() for k in ("title", "focus", "premise", "research_guardrail")), "Incomplete episode")
        require(all(s in sources for s in ep["source_ids"]), "Unknown source reference")
    require(len({ep["title"] for ep in episodes}) == len(episodes), "Duplicate titles")


def plan(data, batch_id):
    validate(data)
    batches = [b for b in data["batches"] if batch_id is None or b["id"] == batch_id]
    require(bool(batches), "Unknown batch")
    ids = [i for b in batches for i in b["episode_ids"]]
    episodes = [ep for ep in data["episodes"] if ep["id"] in ids]
    jobs = []
    for stage in STAGES:
        for ep in episodes:
            idx = STAGES.index(stage)
            job = {"id": f'{ep["id"]}:{stage}', "episode": ep["id"], "stage": stage,
                   "depends_on": [] if idx == 0 else [f'{ep["id"]}:{STAGES[idx-1]}'],
                   "status": "ready_for_research" if idx == 0 else "blocked",
                   "approval_required": stage in PAID_OR_EXTERNAL or stage in {"review"},
                   "source_ids": ep["source_ids"] if idx == 0 else []}
            jobs.append(job)
    return {"series": data["series_id"], "mode": "dry-run", "batches": [b["id"] for b in batches],
            "episodes": ids, "jobs": jobs, "vidiq_credits": 0, "provider_calls": 0,
            "execution_enabled": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT)
    parser.add_argument("--batch", help="Batch ID; omit for all")
    parser.add_argument("--check", action="store_true", help="Validate only")
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
        result = plan(data, args.batch)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        parser.exit(1, f"Invalid plan: {exc}\n")
    if args.check:
        print(f'OK: {len(result["episodes"])} episodes; {len(result["jobs"])} planned jobs; no external calls')
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

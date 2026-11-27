#!/usr/bin/env python3
"""Prepare offline production handoffs. Never calls a provider or publishes."""
import argparse
import hashlib
import json
from pathlib import Path

from check_shorts_visual_identity import validate as validate_visual_identity
from plan_shorts_batch import DEFAULT as SERIES_DEFAULT, validate as validate_series

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "production/series/humanoid-robots-batch-a-drafts.json"
FIELDS = ("hook", "fact", "transition", "fiction", "closing")
VOICE = {"name": "Axel - Natural y Narrativo", "voice_id": "U7je2I3DMxe8ZOLb6vmd", "model_id": "eleven_v4"}
BRAND = {"asset": "CM_Orbita_de_conocimiento_V1.mp4", "seconds": 2.6,
         "sha256": "39851cd9ad858614fc669b729216badd1fececa8d0895a62e175234128b57a7e"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def build(series, drafts):
    validate_series(series)
    validate_visual_identity(drafts)
    require(drafts["schema_version"] == 1, "Unsupported draft schema")
    require(drafts["series_id"] == series["series_id"], "Series mismatch")
    require(drafts["status"] == "draft_for_batch_review", "Expected review drafts")
    require(drafts["vidiq_credits_used"] == 0, "Additional vidIQ spend prohibited")
    require(all(drafts["authorization"][k] is False for k in ("narration", "paid_generation", "gpu_rental", "publication")), "Offline only")
    batches = [b for b in series["batches"] if b["id"] == drafts["batch_id"]]
    require(len(batches) == 1, "Unknown batch")
    episodes = drafts["episodes"]
    require([e["id"] for e in episodes] == batches[0]["episode_ids"], "Episode list mismatch")
    sources = {s["id"]: s for s in drafts["sources"]}
    require(len(sources) == len(drafts["sources"]), "Duplicate source IDs")
    jobs, universe = [], []
    for e in episodes:
        eid, script = e["id"], e["script"]
        require(e["status"] == "draft_for_batch_review", "Episode not a review draft")
        require(set(script) == set(FIELDS), "Unexpected script fields")
        require(all(isinstance(script[k], str) and script[k].strip() for k in FIELDS), "Empty script section")
        require("¿" in script["closing"] and "?" in script["closing"], "Missing closing question")
        require(type(e["future_year"]) is int and e["future_year"] >= 2027, "Invalid fictional year")
        require(str(e["future_year"]) in script["transition"], "Missing explicit fictional year")
        require(e["facts"] and all(f["sources"] and all(s in sources for s in f["sources"]) for f in e["facts"]), "Unmapped claim")
        text = "\n\n".join(script[k].strip() for k in FIELDS)
        require(len(text.split()) == e["word_count"], "Word count mismatch")
        identity = e["visual_identity"]
        h, r = identity["human"], identity["robot"]
        voice_payload = {**VOICE, "text": text}
        key = digest({"episode": eid, "revision": e["script_version"], "payload": voice_payload})
        style = "Ilustración retrofuturista adulta, editorial, crema, verde petróleo y naranja óxido; formato vertical 9:16; sin texto, sin logos."
        human_prompt = f"{style} Ficha de referencia de un personaje ficticio adulto, {h['name']}, {h['age']} años; {h['face']}; {h['hair']}; {h['wardrobe']}. Vistas frontal, tres cuartos y perfil; conservar identidad."
        robot_prompt = f"{style} Ficha de referencia de robot ficticio, {r['role']}; {r['design']}. Vistas frontal, lateral y tres cuartos; conservar silueta y materiales."
        refs = [{"id": h["id"], "prompt": human_prompt}, {"id": r["id"], "prompt": robot_prompt}]
        for ref in refs:
            ref["request_key"] = digest(ref)
            ref["status"] = "blocked_pending_historical_comparison_and_authorization"
        jobs.append({"episode": eid, "title": e["title"], "story_title": e["story_title"],
                     "script_version": e["script_version"], "sections": {k: script[k] for k in FIELDS},
                     "narration": {"request_key": key, "request": voice_payload, "characters": len(text),
                                   "status": "blocked_pending_script_approval_and_spend_authorization",
                                   "provider_called": False},
                     "visual_references": refs, "visual_brief": e["visuals"],
                     "setting": identity["setting"], "composition": identity["composition"],
                     "timing": {"status": "awaiting_actual_audio_alignment", "target_seconds": e["target_duration_s"]},
                     "brand_close": BRAND, "publication": "blocked"})
        universe.append({"episode": eid, "fictional_year": e["future_year"], "human": h, "robot": r,
                         "setting": identity["setting"], "fictional_event": e["fiction"],
                         "connections": [], "canon_status": "proposed_unapproved",
                         "prior_identity_comparison": "pending_S01_S03_and_reserved_EP01"})
    return {"schema_version": 1, "series": drafts["series_id"], "batch": drafts["batch_id"],
            "input_digest": digest({"series": series, "drafts": drafts}), "mode": "offline_preparation",
            "narration_jobs": len(jobs), "reference_jobs": sum(len(j["visual_references"]) for j in jobs),
            "narration_characters": sum(j["narration"]["characters"] for j in jobs),
            "provider_calls": 0, "vidiq_credits": 0, "execution_enabled": False,
            "source_access_note": drafts["source_access_note"], "sources": drafts["sources"],
            "universe": sorted(universe, key=lambda x: (x["fictional_year"], x["episode"])), "episodes": jobs}


def review_markdown(bundle):
    lines = ["# Guiones para revisión editorial", "", "Borradores: no autorizan generación ni publicación.", ""]
    for job in bundle["episodes"]:
        lines.extend([f"## {job['episode']} — {job['story_title']}", "", job["title"], ""])
        for key, label in zip(FIELDS, ("Presente: gancho", "Presente: evidencia", "Transición", "Ficción", "Pregunta final")):
            lines.extend([f"**{label}:** {job['sections'][key]}", ""])
    return "\n".join(lines)


def write_once(path, content):
    # Preserve prior handoffs; changed inputs require a new output directory.
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
    except FileExistsError:
        if path.read_bytes() != content.encode("utf-8"):
            raise ValueError(f"Refusing to overwrite {path}; use a new output directory")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--series", type=Path, default=SERIES_DEFAULT)
    parser.add_argument("--drafts", type=Path, default=DEFAULT)
    parser.add_argument("--output", type=Path, help="Private working directory; omitted for stdout only")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        bundle = build(json.loads(args.series.read_text(encoding="utf-8")), json.loads(args.drafts.read_text(encoding="utf-8")))
        content = json.dumps(bundle, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.mkdir(parents=True, exist_ok=True)
            write_once(args.output / "handoff.json", content)
            write_once(args.output / "guiones.md", review_markdown(bundle))
        if args.check or args.output:
            print(f'OK: {bundle["narration_jobs"]} narration requests, {bundle["reference_jobs"]} reference requests, {bundle["narration_characters"]} characters; 0 provider calls')
        else:
            print(content, end="")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        parser.exit(1, f"Invalid handoff: {exc}\n")


if __name__ == "__main__":
    main()

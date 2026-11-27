#!/usr/bin/env python3
"""Generate caption drafts and timed shot plans from real aligned words."""
import argparse
import csv
import hashlib
import io
import json
import math
import re
from pathlib import Path

FIELDS = ("hook", "fact", "transition", "fiction", "closing")
MAX_LINE = 27
MAX_SECONDS = 3.4
MAX_WORDS = 9
TAIL_TOLERANCE = 0.12


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def norm(text):
    return re.sub(r"[^\w]", "", text.casefold(), flags=re.UNICODE)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def wrap(tokens):
    text = " ".join(tokens)
    if len(text) <= MAX_LINE:
        return text
    options = []
    for i in range(1, len(tokens)):
        a, b = " ".join(tokens[:i]), " ".join(tokens[i:])
        if max(len(a), len(b)) <= MAX_LINE:
            options.append((abs(len(a)-len(b)) + (6 if i == 1 or i == len(tokens)-1 else 0), a, b))
    if not options:
        return None
    _, a, b = min(options)
    return a + "\n" + b


def parse(data):
    sections = data["script_sections"]
    require(set(sections) == set(FIELDS), "Unexpected script sections")
    original = "\n\n".join(sections[k].strip() for k in FIELDS)
    transcript = data["transcript"]
    require(original.split() == transcript["text"].split(), "Transcript differs from the source script")
    words = transcript["words"]
    tokens = original.split()
    require(len(words) == len(tokens) and words, "Incomplete word alignment")
    require([norm(w["text"]) for w in words] == [norm(t) for t in tokens], "Token alignment differs")
    duration = float(data["narration"]["duration_s"])
    require(math.isfinite(duration) and duration > 0, "Invalid audio duration")
    require(float(data["brand_close_seconds"]) == 2.6, "Unexpected brand duration")
    spans = []
    for i, (token, word) in enumerate(zip(tokens, words)):
        start, end = float(word["start"]), float(word["end"])
        require(math.isfinite(start) and math.isfinite(end) and 0 <= start < end, "Invalid word timing")
        require(end <= duration + TAIL_TOLERANCE, "Alignment exceeds audio duration")
        if i:
            require(start >= spans[-1]["start"], "Words out of order")
            require(start >= spans[-1]["end"] - 0.06, "Excessive timing overlap")
        spans.append({"text": token, "start": start, "end": min(end, duration)})
    require(all(w["start"] < w["end"] for w in spans), "Zero-length word after clipping")
    bounds, offset = {}, 0
    for k in FIELDS:
        count = len(sections[k].split())
        require(count > 0, "Empty section")
        bounds[k] = (offset, offset + count)
        offset += count
    return spans, bounds, duration


def captions_for(words):
    # Dynamic programming: keep short readable groups, prefer punctuation boundaries.
    n = len(words)
    best = [None] * (n + 1)
    best[n] = (0, [])
    for i in range(n - 1, -1, -1):
        candidates = []
        for j in range(i + 1, min(n, i + MAX_WORDS) + 1):
            text = wrap([w["text"] for w in words[i:j]])
            if text is None or best[j] is None:
                continue
            start, end = words[i]["start"], words[j-1]["end"]
            if j < n:
                end = min(end, words[j]["start"])
            duration = end - start
            if duration <= 0 or (duration > MAX_SECONDS and j > i + 1):
                continue
            cps = len(text.replace("\n", " ")) / duration
            penalty = 3 + max(0, 0.8-duration)*12 + max(0, cps-22)*0.7
            if j < n and not re.search(r"[.!?,;:]$", words[j-1]["text"]):
                penalty += 1.7
            if j == i+1 and len(words[i]["text"]) < 12:
                penalty += 5
            candidates.append((penalty + best[j][0], [{"start": start, "end": end, "text": text}] + best[j][1]))
        if candidates:
            best[i] = min(candidates, key=lambda x: x[0])
    require(best[0] is not None, "Cannot wrap timed words")
    return best[0][1]


def timestamp(seconds):
    ms = round(seconds*1000)
    hours, rem = divmod(ms, 3600000)
    minutes, rem = divmod(rem, 60000)
    sec, millis = divmod(rem, 1000)
    return f"{hours:02}:{minutes:02}:{sec:02},{millis:03}"


def find_anchor(words, anchor, start, end):
    parts = [norm(t) for t in anchor.split()]
    require(parts and all(parts), "Empty anchor")
    matches = [i for i in range(start, end-len(parts)+1)
               if [norm(w["text"]) for w in words[i:i+len(parts)]] == parts]
    require(len(matches) == 1, f"Missing or ambiguous anchor: {anchor}")
    return matches[0]


def build(data, shot_specs):
    words, bounds, duration = parse(data)
    cues = []
    for k, (a,b) in bounds.items():
        for cue in captions_for(words[a:b]):
            cues.append({"section": k, **cue})
    for i, cue in enumerate(cues):
        if i+1 < len(cues):
            cue["end"] = min(cue["end"], cues[i+1]["start"])
        require(round(cue["end"]*1000) > round(cue["start"]*1000), "Zero-length caption")
        require(all(len(line) <= MAX_LINE for line in cue["text"].splitlines()), "Caption line too long")
    specs = shot_specs["episodes"][data["episode"]]
    shots = []
    previous = -1
    for spec in specs:
        section = spec["section"]
        lo, hi = bounds[section]
        idx = find_anchor(words, spec["anchor"], lo, hi)
        require(idx > previous, "Shot anchors out of order")
        previous = idx
        shots.append({"section": section, "start_s": words[idx]["start"],
                      "anchor": spec["anchor"], "visual": spec["visual"], "technique": spec["technique"]})
    require(shots and shots[0]["section"] == "hook" and previous >= bounds["closing"][0], "Incomplete shot plan")
    require(set(s["section"] for s in shots) == set(FIELDS), "Missing narrative section")
    for section, (lo, hi) in bounds.items():
        first = next(s for s in shots if s["section"] == section)
        require(find_anchor(words, first["anchor"], lo, hi) == lo, f"Section begins without matching visual: {section}")
    shots[0]["start_s"] = 0.0
    for i, shot in enumerate(shots):
        shot["end_s"] = shots[i+1]["start_s"] if i+1 < len(shots) else duration
        require(shot["end_s"] > shot["start_s"], "Invalid shot interval")
        shot["shot_id"] = f"{data['episode']}-P{i+1:02}"
        shot["asset_status"] = "pending"
    shots.append({"shot_id": f"{data['episode']}-BRAND", "section": "brand", "start_s": duration,
                  "end_s": round(duration+2.6,3), "anchor": "", "visual": "Cierre oficial Órbita de conocimiento",
                  "technique": "approved_brand_asset", "asset_status": "hash_verification_pending"})
    warnings = []
    for i, cue in enumerate(cues, 1):
        length = cue["end"]-cue["start"]
        if length < 0.6 or len(cue["text"].replace("\n"," "))/length > 24:
            warnings.append(f"Caption {i}: check reading speed/short duration")
    for shot in shots[:-1]:
        if shot["end_s"]-shot["start_s"] > 5.5 or shot["end_s"]-shot["start_s"] < 1.0:
            warnings.append(f"{shot['shot_id']}: check pacing")
    srt = "\n".join(f"{i}\n{timestamp(c['start'])} --> {timestamp(c['end'])}\n{c['text']}\n" for i,c in enumerate(cues,1))
    report = {"episode": data["episode"], "narration": data["narration"],
              "transcript_id": data["transcript"]["generation_id"], "audio_seconds": duration,
              "final_target_seconds": round(duration+2.6,3), "caption_count": len(cues),
              "shot_count_including_brand": len(shots), "warnings": warnings,
              "status": "draft_timing_not_visual_approval"}
    return srt, shots, report


def write_once(path, content):
    encoded = content.encode("utf-8")
    try:
        with path.open("xb") as f:
            f.write(encoded)
    except FileExistsError:
        require(path.read_bytes() == encoded, f"Existing different file: {path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--shots", required=True, type=Path)
    parser.add_argument("--audio", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        require(sha256_file(args.audio) == data["narration"]["sha256"], "Audio hash mismatch")
        srt, shots, report = build(data, json.loads(args.shots.read_text(encoding="utf-8")))
        args.output.mkdir(parents=True, exist_ok=True)
        out = io.StringIO(newline="")
        writer = csv.DictWriter(out, fieldnames=["shot_id","section","start_s","end_s","anchor","visual","technique","asset_status"])
        writer.writeheader()
        writer.writerows(shots)
        write_once(args.output / "subtitulos.srt", srt)
        write_once(args.output / "storyboard.csv", out.getvalue())
        write_once(args.output / "timing-report.json", json.dumps(report,ensure_ascii=False,indent=2)+"\n")
        print(json.dumps(report, ensure_ascii=True))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        parser.exit(1, f"Invalid timing inputs: {exc}\n")


if __name__ == "__main__":
    main()

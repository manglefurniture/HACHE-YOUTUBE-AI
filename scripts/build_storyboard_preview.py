#!/usr/bin/env python3
"""GPU-free storyboard video with placeholder cards and optional narration WAV.

Usage: python3 scripts/build_storyboard_preview.py --output preview.mp4
       python3 scripts/build_storyboard_preview.py --voice narration.wav --output preview.mp4
Requires ffmpeg/ffprobe on PATH; no third-party Python packages.
The optional voice must be authorized and is mixed with silence if shorter than 75s.
"""
import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

SCENES = [
    ("S01", 12, "CIUDAD AL AMANECER"),
    ("S02", 13, "FABRICA AUTONOMA"),
    ("S03", 15, "MARA Y SU CREDENCIAL"),
    ("S04", 15, "HIPOTESIS: TECNOLOGIA Y SOCIEDAD"),
    ("S05", 20, "LA PLAZA Y LA DECISION"),
]

def run(args):
    subprocess.run(args, check=True)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, default=Path("preview.mp4"))
    p.add_argument("--voice", type=Path)
    a = p.parse_args()
    if not shutil.which("ffmpeg"):
        p.error("ffmpeg no esta instalado")
    if a.voice and not a.voice.is_file():
        p.error("no existe el archivo de narracion")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        clips = []
        for index, (sid, duration, label) in enumerate(SCENES):
            target = Path(td) / f"{index:02}.mp4"
            # Static placeholder: no external fonts, image models or downloaded assets.
            run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                 "-f", "lavfi", "-i", f"color=c=0x17202a:s=1280x720:r=24:d={duration}",
                 "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                 "-an", str(target)])
            clips.append((target, sid, label, duration))
        concat = Path(td) / "concat.txt"
        concat.write_text("".join(f"file '{clip.as_posix()}'\n" for clip, _, _, _ in clips), encoding="utf-8")
        joined = Path(td) / "joined.mp4"
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
             "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(joined)])
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(joined)]
        if a.voice:
            cmd += ["-i", str(a.voice), "-filter_complex", "[1:a]apad=whole_dur=75,atrim=duration=75[a]",
                    "-map", "0:v:0", "-map", "[a]"]
        else:
            cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v:0", "-map", "1:a:0"]
        cmd += ["-t", "75", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(a.output)]
        run(cmd)
        print(f"Preview: {a.output} (75 s, placeholders only)")
        for _, sid, label, duration in clips:
            print(f"{sid}: {label} ({duration}s)")

if __name__ == "__main__":
    main()

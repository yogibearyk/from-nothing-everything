#!/usr/bin/env python3
"""
From Nothing, Everything — Video Generator
==========================================

Converts chapter HTML presentations + narration scripts into
full videos with AI-generated narration.

Requirements (install once):
    pip install edge-tts pillow

System requirements:
    - ffmpeg (brew install ffmpeg / apt install ffmpeg)
    - Python 3.8+

Usage:
    python make_video.py chapter_01              # single chapter
    python make_video.py all                     # all chapters
    python make_video.py chapter_01 --voice en-GB-RyanNeural  # different voice

Voices (warm male recommendations):
    en-US-GuyNeural        — American, warm, conversational
    en-GB-RyanNeural       — British, calm, authoritative
    en-US-ChristopherNeural — American, deeper
    en-AU-WilliamNeural    — Australian, friendly
"""

import asyncio
import json
import os
import re
import sys
import subprocess
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Install Pillow: pip install pillow")
    sys.exit(1)

try:
    import edge_tts
except ImportError:
    print("Install edge-tts: pip install edge-tts")
    sys.exit(1)


# ============================================================
# CONFIGURATION
# ============================================================

WIDTH, HEIGHT = 1920, 1080
BG_COLOR = (10, 10, 15)
TEXT_COLOR = (208, 208, 216)
ACCENT_COLOR = (240, 192, 64)
DIM_COLOR = (136, 136, 152)
HEADING_COLOR = (200, 200, 210)

DEFAULT_VOICE = "en-US-GuyNeural"
RATE = "-5%"          # slightly slower for clarity
PITCH = "-2Hz"        # slightly deeper for warmth
PAUSE_AFTER = 1.5     # seconds of silence after each slide's narration


# ============================================================
# SLIDE DATA — Chapter 1 (extend for more chapters)
# ============================================================

CHAPTERS = {
    "chapter_01": {
        "title": "Chapter 1 — The Ground: Ω",
        "slides": [
            {
                "lines": [
                    ("FROM NOTHING, EVERYTHING", "chapter_num"),
                    ("Chapter 1", "h1"),
                    ("The Ground: Ω", "h2"),
                    ("Axiom 1", "small"),
                ],
                "narration": "Welcome to From Nothing, Everything. This is Chapter 1: The Ground. We begin at the only place we can — before anything exists at all.",
            },
            {
                "lines": [
                    ("What is the least that has to be true", "p"),
                    ("for anything to be true at all?", "p"),
                ],
                "narration": "We start with one question: what is the least that has to be true for anything to be true at all? Not what existed before the Big Bang — that assumes time already exists. Not what caused the universe — that assumes cause and effect. Something more basic. Something underneath all of those ideas.",
            },
            {
                "lines": [
                    ("Ω", "omega"),
                    ("A state with no structure.", "p"),
                    ("No space. No time. No distinction.", "p"),
                ],
                "narration": "We call this starting point Omega. It is a state with no structure at all. No space, no time, no way to tell zero from one. Not empty the way an empty room is empty — an empty room still has walls and dimensions. Omega has none of these.",
            },
            {
                "lines": [
                    ("0 = 1 = ∞", "equation"),
                    ("Without any distinction,", "p"),
                    ("these are not three things but one.", "p"),
                ],
                "narration": "Without any distinction, zero and one and infinity are not three different things. They collapse into one — not because they are equal in the mathematical sense, but because the machinery that would separate them does not exist yet. Equality is itself a distinction, and there are no distinctions.",
            },
            {
                "lines": [
                    ("Nothing from outside", "h2"),
                    ("There is no outside.", "p"),
                    ("Whatever emerges must be built entirely", "p"),
                    ("from the act of self-examination itself.", "p"),
                ],
                "narration": "And here is the crucial constraint — the one that makes everything else possible. There is no outside. Whatever emerges from Omega must be built entirely from the act of self-examination itself. No imported materials, no borrowed constants, no pre-existing mathematics. If there were an outside, there would be choices. If there were choices, there would be parameters. And if there were parameters, we would need experiments to measure them.",
            },
            {
                "lines": [
                    ("By starting from a ground", "p"),
                    ("that genuinely contains nothing,", "p"),
                    ("the framework eliminates free parameters", "accent"),
                    ("at the root.", "accent"),
                ],
                "narration": "By starting from a ground that genuinely contains nothing, the framework eliminates the possibility of free parameters at the root. Everything that follows — every force, every particle, every number — is a consequence, not a choice. The first ratio will not be chosen from a menu of possibilities. It will be the only ratio consistent with a structure that must build itself from nothing.",
            },
            {
                "lines": [
                    ("Each act of self-examination", "p"),
                    ("builds on the last,", "p"),
                    ("creating a structure called a tower —", "p_italic"),
                    ("a stack of nested lenses,", "p"),
                    ("each screening what the one above can see.", "p"),
                ],
                "narration": "In the chapters ahead, each act of self-examination builds on the last, creating a structure the framework calls a tower. Think of it as a stack of nested lenses, each one containing the ones below. The first resolves one distinction, then two, then three, five, eight — growing by the Fibonacci sequence. Each lens screens what the one above can see, dimming it by a precise fraction.",
            },
            {
                "lines": [
                    ("Every particle — every electron,", "p"),
                    ("every photon, every quark —", "p"),
                    ("is one of these towers.", "accent"),
                    ("A glass of water holds 10²⁵ of them.", "small"),
                ],
                "narration": "That is not a metaphor. Every particle — every electron orbiting an atom, every photon of light, every quark inside a proton — is one of these towers, running the same self-examining arithmetic from the ground up. A single glass of water contains roughly ten trillion trillion of them. Each one identical in architecture, each one built from the golden ratio.",
            },
            {
                "lines": [
                    ("The universe is not made of towers", "p"),
                    ("the way a wall is made of bricks.", "p"),
                    ("The universe is towers —", "accent_large"),
                    ("the way a symphony is sound waves.", "p"),
                ],
                "narration": "The universe, in this picture, is not made of towers the way a wall is made of bricks. The universe IS towers — the way a symphony is sound waves. Not a thing that has sound waves, but a thing that is sound waves, all the way down.",
            },
            {
                "lines": [
                    ("Axiom 1", "h3"),
                    ("Ω exists, in which 0 = 1 = ∞", "equation"),
                    ("Pre-geometric: no shape, no dimensions.", "p"),
                    ("The silence before the music.", "small"),
                ],
                "narration": "And so we arrive at Axiom 1 — the first and simplest of the ten. Omega exists, in which zero equals one equals infinity. Pre-geometric: no shape, no dimensions. This is the blank page. The silence before the music. The first note — the first distinction — comes in the next chapter.",
            },
            {
                "lines": [
                    ("FROM NOTHING, EVERYTHING", "chapter_num"),
                    ("Next: Chapter 2", "h2"),
                    ("The First Distinction,", "p"),
                    ("and the Birth of ⊙", "p"),
                ],
                "narration": "Next: Chapter 2 — The First Distinction, and the Birth of the circle constant. The silence is about to break.",
            },
        ],
    },
}


# ============================================================
# RENDERING ENGINE
# ============================================================

def get_font(size, bold=False, italic=False):
    """Try to load a good font, fall back to default."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "/usr/share/fonts/TTF/DejaVuSerif.ttf",
    ]
    if bold:
        candidates = [c.replace(".ttf", "-Bold.ttf").replace("Regular", "Bold") for c in candidates] + candidates
    if italic:
        candidates = [c.replace(".ttf", "-Italic.ttf").replace("Regular", "Italic") for c in candidates] + candidates

    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()


STYLES = {
    "h1":           {"size": 80, "color": (240, 240, 240), "bold": True},
    "h2":           {"size": 56, "color": HEADING_COLOR},
    "h3":           {"size": 36, "color": DIM_COLOR, "italic": True},
    "p":            {"size": 38, "color": TEXT_COLOR},
    "p_italic":     {"size": 38, "color": TEXT_COLOR, "italic": True},
    "small":        {"size": 28, "color": DIM_COLOR},
    "accent":       {"size": 40, "color": ACCENT_COLOR},
    "accent_large": {"size": 44, "color": ACCENT_COLOR},
    "equation":     {"size": 72, "color": ACCENT_COLOR, "italic": True},
    "omega":        {"size": 120, "color": (136, 136, 170), "italic": True},
    "chapter_num":  {"size": 22, "color": (85, 85, 112)},
}


def render_slide(slide_data, output_path):
    """Render a single slide to an image."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    lines = slide_data["lines"]
    total_height = 0
    rendered_lines = []

    for text, style_name in lines:
        style = STYLES.get(style_name, STYLES["p"])
        font = get_font(style["size"], style.get("bold"), style.get("italic"))
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        rendered_lines.append((text, font, style["color"], w, h))
        total_height += h + 20  # line spacing

    # Center vertically
    y = (HEIGHT - total_height) // 2
    for text, font, color, w, h in rendered_lines:
        x = (WIDTH - w) // 2
        draw.text((x, y), text, fill=color, font=font)
        y += h + 20

    # Add subtle bottom progress line (optional)
    img.save(output_path, "PNG")


# ============================================================
# AUDIO GENERATION
# ============================================================

async def generate_narration(text, output_path, voice=DEFAULT_VOICE):
    """Generate narration audio using Edge TTS."""
    communicate = edge_tts.Communicate(text, voice, rate=RATE, pitch=PITCH)
    await communicate.save(output_path)


# ============================================================
# VIDEO ASSEMBLY
# ============================================================

def make_chapter_video(chapter_key, voice=DEFAULT_VOICE):
    """Generate a complete chapter video."""
    chapter = CHAPTERS[chapter_key]
    slides = chapter["slides"]
    work_dir = Path(f"video/build/{chapter_key}")
    work_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*50}")
    print(f"  {chapter['title']}")
    print(f"{'='*50}")

    # Step 1: Render slides
    print("\n  [1/3] Rendering slides...")
    for i, slide in enumerate(slides):
        img_path = work_dir / f"slide_{i:03d}.png"
        render_slide(slide, str(img_path))
        print(f"    ✓ Slide {i+1}/{len(slides)}")

    # Step 2: Generate narration
    print("\n  [2/3] Generating narration...")
    audio_files = []
    for i, slide in enumerate(slides):
        audio_path = work_dir / f"narration_{i:03d}.mp3"
        asyncio.run(generate_narration(slide["narration"], str(audio_path), voice))
        audio_files.append(audio_path)
        print(f"    ✓ Audio {i+1}/{len(slides)}")

    # Step 3: Combine into video
    print("\n  [3/3] Assembling video...")

    # Get duration of each audio file
    segments = []
    for i, (slide, audio_path) in enumerate(zip(slides, audio_files)):
        # Get audio duration
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "json", str(audio_path)],
            capture_output=True, text=True
        )
        duration = float(json.loads(result.stdout)["format"]["duration"]) + PAUSE_AFTER
        img_path = work_dir / f"slide_{i:03d}.png"
        segments.append((str(img_path), str(audio_path), duration))

    # Create concat file for ffmpeg
    concat_file = work_dir / "concat.txt"
    filter_parts = []
    inputs = []

    for i, (img, audio, dur) in enumerate(segments):
        inputs.extend(["-loop", "1", "-t", f"{dur:.2f}", "-i", img])
        inputs.extend(["-i", audio])

    # Build filter complex
    n = len(segments)
    video_filters = []
    audio_filters = []
    for i in range(n):
        vi = i * 2      # video input index
        ai = i * 2 + 1  # audio input index
        # Add fade in/out to each slide
        video_filters.append(
            f"[{vi}:v]scale={WIDTH}:{HEIGHT},fade=in:0:15,fade=out:st={segments[i][2]-0.5}:d=0.5[v{i}]"
        )
        # Pad audio to match slide duration
        audio_filters.append(
            f"[{ai}:a]apad,atrim=0:{segments[i][2]:.2f}[a{i}]"
        )

    # Concat all
    v_concat = "".join(f"[v{i}]" for i in range(n))
    a_concat = "".join(f"[a{i}]" for i in range(n))
    filter_complex = ";".join(video_filters + audio_filters) + \
        f";{v_concat}concat=n={n}:v=1:a=0[vout];{a_concat}concat=n={n}:v=0:a=1[aout]"

    output_path = f"video/{chapter_key}.mp4"
    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_complex,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"\n  ✅ Video created: {output_path} ({size_mb:.1f} MB)")
    else:
        print(f"\n  ❌ ffmpeg error: {result.stderr[-500:]}")
        # Fall back to simpler approach
        print("  Trying simpler assembly...")
        simple_assemble(segments, output_path)

    return output_path


def simple_assemble(segments, output_path):
    """Simpler ffmpeg approach if the complex filter fails."""
    work_dir = Path(output_path).parent / "build" / Path(output_path).stem
    
    # Create individual segment videos first
    part_files = []
    for i, (img, audio, dur) in enumerate(segments):
        part = str(work_dir / f"part_{i:03d}.mp4")
        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-t", f"{dur:.2f}", "-i", img,
            "-i", audio,
            "-c:v", "libx264", "-preset", "fast", "-crf", "25",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            "-shortest", part
        ], capture_output=True)
        part_files.append(part)

    # Concat
    list_file = str(work_dir / "parts.txt")
    with open(list_file, "w") as f:
        for p in part_files:
            f.write(f"file '{p}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-c", "copy", output_path
    ], capture_output=True)

    if os.path.exists(output_path):
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  ✅ Video created (simple): {output_path} ({size_mb:.1f} MB)")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    voice = DEFAULT_VOICE

    # Parse args
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        print("Available chapters:", ", ".join(CHAPTERS.keys()))
        sys.exit(0)

    chapter = args[0]
    for i, arg in enumerate(args):
        if arg == "--voice" and i + 1 < len(args):
            voice = args[i + 1]

    if chapter == "all":
        for key in CHAPTERS:
            make_chapter_video(key, voice)
    elif chapter in CHAPTERS:
        make_chapter_video(chapter, voice)
    else:
        print(f"Unknown chapter: {chapter}")
        print("Available:", ", ".join(CHAPTERS.keys()))

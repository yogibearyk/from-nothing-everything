#!/usr/bin/env python3
"""
From Nothing, Everything — Video Series Generator
===================================================

Creates narrated video chapters using Speechify's Benjamin voice.

Setup:
    1. pip install speechify-api pillow
    2. Get API key from https://console.speechify.ai/api-keys
    3. export SPEECHIFY_API_KEY="your-key-here"
    4. Ensure ffmpeg is installed

Usage:
    python make_videos.py chapter_01           # single chapter
    python make_videos.py all                  # all chapters
    python make_videos.py chapter_01 --dry-run # render slides only, no audio
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ============================================================
# CONFIGURATION
# ============================================================

WIDTH, HEIGHT = 1920, 1080
BG_COLOR = (10, 10, 15)
TEXT_COLOR = (208, 208, 216)
ACCENT_COLOR = (240, 192, 64)
DIM_COLOR = (136, 136, 152)
HEADING_COLOR = (200, 200, 210)

SPEECHIFY_VOICE = "benjamin"
SPEECHIFY_MODEL = "simba-english"
AUDIO_FORMAT = "mp3"
PAUSE_AFTER_SLIDE = 1.5  # seconds of silence between slides

VIDEOS_DIR = Path(__file__).parent
SLIDES_DIR = VIDEOS_DIR / "slides"
NARRATION_DIR = VIDEOS_DIR / "narration"
OUTPUT_DIR = VIDEOS_DIR / "output"
BUILD_DIR = VIDEOS_DIR / "build"


# ============================================================
# TEXT STYLES
# ============================================================

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


# ============================================================
# FONT LOADING
# ============================================================

def get_font(size, bold=False, italic=False):
    """Load the best available serif font."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "/System/Library/Fonts/Times.ttc",
        "/Library/Fonts/Times New Roman.ttf",
        "C:\\Windows\\Fonts\\times.ttf",
    ]
    if bold:
        candidates = [c.replace(".ttf", "-Bold.ttf").replace("Regular", "Bold")
                      for c in candidates] + candidates
    if italic:
        candidates = [c.replace(".ttf", "-Italic.ttf").replace("Regular", "Italic")
                      for c in candidates] + candidates
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


# ============================================================
# SLIDE RENDERER
# ============================================================

def render_slide(slide_data, output_path):
    """Render a single slide as a 1920x1080 PNG."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    lines = slide_data["lines"]
    rendered = []
    total_h = 0

    for text, style_name in lines:
        style = STYLES.get(style_name, STYLES["p"])
        font = get_font(style["size"], style.get("bold"), style.get("italic"))
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        rendered.append((text, font, style["color"], w, h))
        total_h += h + 24

    y = (HEIGHT - total_h) // 2
    for text, font, color, w, h in rendered:
        x = (WIDTH - w) // 2
        draw.text((x, y), text, fill=color, font=font)
        y += h + 24

    img.save(output_path, "PNG")


# ============================================================
# SPEECHIFY TTS
# ============================================================

def generate_audio(text, output_path):
    """Generate narration audio using Speechify's Benjamin voice."""
    try:
        from speechify import Speechify
    except ImportError:
        print("  ⚠ speechify-api not installed. Run: pip install speechify-api")
        print("    Falling back to silent slides.")
        return generate_silence(5.0, output_path)

    api_key = os.environ.get("SPEECHIFY_API_KEY")
    if not api_key:
        print("  ⚠ SPEECHIFY_API_KEY not set. Get one at https://console.speechify.ai/api-keys")
        print("    Falling back to silent slides.")
        return generate_silence(5.0, output_path)

    client = Speechify(api_key=api_key)
    response = client.tts.audio.speech(
        input=text,
        voice_id=SPEECHIFY_VOICE,
        audio_format=AUDIO_FORMAT,
    )

    mp3_path = output_path.replace(".wav", ".mp3")
    with open(mp3_path, "wb") as f:
        f.write(response.audio_data)

    # Convert to wav for consistent ffmpeg handling
    subprocess.run([
        "ffmpeg", "-y", "-i", mp3_path, output_path
    ], capture_output=True)

    return output_path


def generate_silence(duration, output_path):
    """Generate a silent audio file as fallback."""
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i",
        f"anullsrc=r=44100:cl=mono", "-t", str(duration),
        output_path
    ], capture_output=True)
    return output_path


# ============================================================
# VIDEO ASSEMBLY
# ============================================================

def get_audio_duration(path):
    """Get duration of an audio file in seconds."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "json", path],
        capture_output=True, text=True
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def make_chapter_video(chapter_key, dry_run=False):
    """Generate a complete chapter video."""
    data_path = NARRATION_DIR / f"{chapter_key}.json"
    if not data_path.exists():
        print(f"  ✗ No data file: {data_path}")
        return None

    chapter = json.loads(data_path.read_text())
    slides = chapter["slides"]
    title = chapter["title"]

    work = BUILD_DIR / chapter_key
    work.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")

    # Step 1: Render slides
    print(f"\n  [1/3] Rendering {len(slides)} slides...")
    for i, slide in enumerate(slides):
        img_path = work / f"slide_{i:03d}.png"
        render_slide(slide, str(img_path))
        print(f"    ✓ Slide {i + 1}/{len(slides)}: {slide['lines'][0][0][:40]}...")

    if dry_run:
        print("\n  [dry-run] Slides rendered. Skipping audio and video.")
        return None

    # Step 2: Generate narration
    print(f"\n  [2/3] Generating narration (Speechify — {SPEECHIFY_VOICE})...")
    audio_files = []
    for i, slide in enumerate(slides):
        audio_path = str(work / f"narration_{i:03d}.wav")
        generate_audio(slide["narration"], audio_path)
        audio_files.append(audio_path)
        print(f"    ✓ Audio {i + 1}/{len(slides)}")

    # Step 3: Assemble video
    print(f"\n  [3/3] Assembling video...")
    parts = []
    for i in range(len(slides)):
        img = str(work / f"slide_{i:03d}.png")
        audio = audio_files[i]
        part = str(work / f"part_{i:03d}.mp4")

        dur = get_audio_duration(audio) + PAUSE_AFTER_SLIDE

        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-t", f"{dur:.1f}", "-i", img,
            "-i", audio,
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
            "-t", f"{dur:.1f}", part
        ], capture_output=True)
        parts.append(part)

    # Concatenate
    list_file = str(work / "parts.txt")
    with open(list_file, "w") as f:
        for p in parts:
            f.write(f"file '{os.path.abspath(p)}'\n")

    output = str(OUTPUT_DIR / f"{chapter_key}.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
        "-c", "copy", output
    ], capture_output=True)

    if os.path.exists(output):
        size_mb = os.path.getsize(output) / (1024 * 1024)
        duration = get_audio_duration(output)
        print(f"\n  ✅ {output}")
        print(f"     {size_mb:.1f} MB | {duration:.0f}s ({duration / 60:.1f} min)")
        return output
    else:
        print(f"\n  ❌ Video creation failed")
        return None


# ============================================================
# MAIN
# ============================================================

def list_chapters():
    """List all available chapter data files."""
    files = sorted(NARRATION_DIR.glob("*.json"))
    for f in files:
        data = json.loads(f.read_text())
        print(f"  {f.stem:20s} — {data['title']} ({len(data['slides'])} slides)")
    if not files:
        print("  No chapter data files found in videos/narration/")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        print("\nAvailable chapters:")
        list_chapters()
        sys.exit(0)

    dry_run = "--dry-run" in args
    chapter = args[0]

    if chapter == "all":
        files = sorted(NARRATION_DIR.glob("*.json"))
        for f in files:
            make_chapter_video(f.stem, dry_run)
    elif chapter == "list":
        list_chapters()
    else:
        make_chapter_video(chapter, dry_run)

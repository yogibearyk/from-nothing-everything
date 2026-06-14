# Video Generation Prompt for Claude Opus 4.6 (Cursor)

Copy everything below the line into a new Claude session in Cursor.

---

## Context

I'm working on the book "From Nothing, Everything" — a zero-free-parameter physics framework. The book is in two GitHub repos:

- **Private:** `yogibearyk/maya-chakra-math`
- **Public:** `yogibearyk/from-nothing-everything`

Both repos contain a `videos/` folder with everything needed to generate a 31-chapter narrated video series.

## What exists

```
videos/
  make_videos.py              ← Python script that generates videos
  narration/
    chapter_01.json            ← slide data + narration for each chapter
    chapter_02.json
    ...
    chapter_31.json
  slides/                     ← HTML presentations (Chapter 1)
  output/                     ← where generated .mp4 files go
  build/                      ← temporary build files
  README.md
```

Each `chapter_XX.json` contains:
```json
{
  "title": "Chapter X — Title",
  "slides": [
    {
      "lines": [["text", "style"], ...],
      "narration": "spoken text for this slide"
    },
    ...
  ]
}
```

## What I need you to do

1. Clone the private repo: `git clone https://github.com/yogibearyk/maya-chakra-math.git`
2. `cd maya-chakra-math/videos`
3. Install dependencies: `pip install speechify-api pillow`
4. Verify my Speechify API key is set: `echo $SPEECHIFY_API_KEY`
   - If not set: `export SPEECHIFY_API_KEY="<my key>"`
   - Get a key from https://console.speechify.ai/api-keys if needed
5. Verify ffmpeg is installed: `which ffmpeg`
6. Do a dry run first to test slides: `python make_videos.py intro --dry-run`
7. Generate the Introduction with Benjamin's voice: `python make_videos.py intro`
8. If it looks and sounds good, generate all 33 segments: `python make_videos.py all`
9. Commit the output videos to both repos and push

## Technical details

- **TTS:** Speechify API, voice_id="benjamin", model="simba-english"
- **Video:** 1920×1080, dark background (#0a0a0f), serif font, gold accents (#f0c040)
- **Assembly:** ffmpeg, libx264, AAC audio, 1.5s pause between slides
- **Slides:** Rendered with Pillow (PIL) as PNG images from the JSON data

## If something goes wrong

- **Speechify API error:** Check the API key is valid and has credits. The free tier may have limits.
- **ffmpeg not found:** Install with `brew install ffmpeg` (Mac) or `sudo apt install ffmpeg` (Linux)
- **Font rendering issues:** The script tries DejaVu Serif, Liberation Serif, and Times New Roman. Install one if none are found: `brew install font-dejavu` or `sudo apt install fonts-dejavu`
- **Audio sync issues:** Adjust `PAUSE_AFTER_SLIDE` in make_videos.py (default 1.5s)

## After generation

- Videos will be in `videos/output/` — intro.mp4, part_00.mp4, chapter_01.mp4 through chapter_31.mp4 (33 total)
- Commit to private repo: `git add -A && git commit -m "Generated 31 chapter videos with Benjamin voice" && git push`
- Copy to public repo and push there too
- Total estimated: ~2 hours of video, ~31 files, ~100-200 MB total

## Git identity for commits

```
git config user.name "Maya-Agent"
git config user.email "maya-agent@binfinite.com"
```

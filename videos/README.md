# From Nothing, Everything — Video Series

31 chapter videos with AI-narrated slides using Speechify's Benjamin voice.

## Quick Start

```bash
# 1. Install dependencies
pip install speechify-api pillow

# 2. Set your Speechify API key
export SPEECHIFY_API_KEY="your-key-from-console.speechify.ai"

# 3. Generate a single chapter
python make_videos.py chapter_01

# 4. Generate all chapters
python make_videos.py all

# 5. List available chapters
python make_videos.py list
```

## Structure

```
videos/
  make_videos.py           ← main script (run this)
  narration/               ← chapter data (slides + narration text)
    chapter_01.json
    chapter_02.json
    ...
    chapter_31.json
  slides/                  ← HTML presentation versions
  output/                  ← generated .mp4 files (after running)
  build/                   ← temporary build files
```

## Voice

Uses Speechify's **Benjamin** voice (simba-english model).
Get an API key at https://console.speechify.ai/api-keys

## Dry Run (no API key needed)

```bash
python make_videos.py chapter_01 --dry-run
```

This renders the slide images without generating audio, so you can
preview the visuals before using API credits.

# Generate Summary Video — Prompt for Claude Opus 4.6 (Cursor)

Copy everything below the line into a new Claude session in Cursor.

---

## Task

Generate the summary video "From Nothing, Everything — The Essence" using the existing video pipeline in the `maya-chakra-math` repo.

## Steps

1. Clone the repo:
```bash
git clone https://github.com/yogibearyk/maya-chakra-math.git
cd maya-chakra-math
git config user.name "Maya-Agent"
git config user.email "maya-agent@binfinite.com"
```

2. Install dependencies:
```bash
pip install speechify-api pillow
```

3. Verify ffmpeg:
```bash
which ffmpeg || echo "Install ffmpeg: brew install ffmpeg (Mac) or sudo apt install ffmpeg (Linux)"
```

4. Set the Speechify API key:
```bash
export SPEECHIFY_API_KEY="<paste your key here>"
```
Get a key from https://console.speechify.ai/api-keys if you don't have one.

5. Test with a dry run (renders slides only, no API calls):
```bash
cd videos
python make_videos.py summary --dry-run
```
Verify that 23 slide images appear in `videos/build/summary/`.

6. Generate the full video with Benjamin's voice:
```bash
python make_videos.py summary
```
This will:
- Render 23 dark cinematic slides (1920×1080)
- Call Speechify API with Benjamin's voice (simba-english model) for each slide's narration
- Sync audio to slides with 1.5s pauses between slides
- Assemble into `videos/output/summary.mp4` using ffmpeg

7. Verify the output:
```bash
ls -lh videos/output/summary.mp4
ffprobe -v quiet -show_entries format=duration -of json videos/output/summary.mp4
```
Expected: ~12 minutes, ~20-40 MB.

8. If it looks good, also generate the intro and part 0:
```bash
python make_videos.py intro
python make_videos.py part_00
```

9. To generate ALL 34 segments (summary + intro + part_00 + 31 chapters):
```bash
python make_videos.py all
```

10. Commit and push:
```bash
cd ..
git add -A
git commit -m "Generated summary video with Benjamin voice"
git push
```

11. Also update the public repo:
```bash
cd ..
git clone https://github.com/yogibearyk/from-nothing-everything.git
cp -r maya-chakra-math/videos/output from-nothing-everything/videos/
cd from-nothing-everything
git add -A
git commit -m "Generated videos"
git push
```

## Troubleshooting

**Speechify API error / 401:**
- Verify key: `echo $SPEECHIFY_API_KEY`
- Check credits at https://console.speechify.ai
- The voice_id is "benjamin" and model is "simba-english"

**Font rendering — text looks wrong:**
- Install DejaVu fonts: `brew install font-dejavu` (Mac) or `sudo apt install fonts-dejavu` (Linux)
- Or install Liberation fonts: `sudo apt install fonts-liberation`

**ffmpeg errors:**
- Ensure ffmpeg supports libx264: `ffmpeg -codecs | grep x264`
- On Mac: `brew install ffmpeg`

**Slides render but audio is silent:**
- The script falls back to silent audio if Speechify fails
- Check the console output for "⚠ speechify-api" warnings
- Verify internet connectivity to speechify.com

## What the summary video contains

23 slides telling the complete story in ~12 minutes:
- Acts 1-2: The experiential hook + Advaitic roots
- Acts 3-4: Omega, the ground, the "nothing from outside" constraint
- Acts 5-6: The golden ratio (forced, not chosen) + the Fibonacci tower
- Acts 7-8: The physical world (glass of water, symphony metaphor)
- Acts 9-10: The stunning predictions (α to 8 figures, v to 0.66 ppm)
- Act 11: The CMB — 2,500 data points, zero knobs
- Acts 12-13: Dark matter (stage 7) + the φ² formula (E=mc²)
- Closing: The wager, the book link, "the silence examined itself"

All narration data is in `videos/narration/summary.json`.
All slide rendering + video assembly code is in `videos/make_videos.py`.

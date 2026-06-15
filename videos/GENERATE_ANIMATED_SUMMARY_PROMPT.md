# Generate Animated Summary Video — Prompt for Claude Opus 4.6 (Cursor)

Copy everything below the line into a new Claude session in Cursor.

---

## Task

Generate the animated summary video "From Nothing, Everything — The Essence" using the HTML presentation and Speechify's Benjamin voice. The video should include meaningful pauses after key revelations to let the viewer absorb the concepts.

## Setup

```bash
git clone https://github.com/yogibearyk/maya-chakra-math.git
cd maya-chakra-math
git config user.name "Maya-Agent"
git config user.email "maya-agent@binfinite.com"

pip install speechify-api pillow selenium
export SPEECHIFY_API_KEY="<paste your key here>"
```

You also need:
- ffmpeg: `brew install ffmpeg` (Mac) or `sudo apt install ffmpeg`
- Chrome + chromedriver for screenshot capture: `brew install chromedriver` or `pip install chromedriver-autoinstaller`

## The Presentation

The animated HTML is at: `videos/slides/summary_animated.html`

It has 15 slides, each with SVG animations and a hidden `<div class="narration">` containing the spoken text. Open it in Chrome to preview — click or arrow-key to advance.

## Video Generation Approach

For each slide:
1. Open the HTML in a headless Chrome browser at 1920×1080
2. Navigate to that slide and wait for animations to complete
3. Capture a screenshot (or screen-record the animation duration)
4. Generate the narration audio using Speechify Benjamin voice
5. Combine the image + audio + pauses into a video segment
6. Concatenate all segments into the final video

If you can capture the SVG ANIMATIONS as video (using screen recording or puppeteer), that's ideal. If not, fall back to static screenshots — the narration will carry the story.

## Slide-by-Slide Specification

Each entry below gives: the slide number, the narration text, the animation wait time (how long to let the SVG animation play before capturing), and the pause duration AFTER the narration finishes (silence for the viewer to absorb).

### Slide 1 — Title (animation: 2s, pause after: 2s)
**Narration:** "Welcome to From Nothing, Everything. This is the story of a single idea: a wholeness that examines itself, and in doing so, gives rise to everything."

### Slide 2 — Close Your Eyes (animation: 3s, pause after: 3s)
**Narration:** "Close your eyes for a moment and notice that you are aware. Not aware of anything in particular — just aware. Now notice something strange: you are the one noticing. Before that second thought, there was just experience, undivided. After it, there are two: a watcher and the watched. And yet they haven't separated. The watcher IS the watched, turned back on itself."
**Note:** This is the experiential hook. The 3-second pause lets the viewer sit with the feeling.

### Slide 3 — The Ancient Question (animation: 4s, pause after: 2s)
**Narration:** "Three thousand years ago, Indian philosophers in the Advaitic tradition proposed exactly this. Reality begins as an undifferentiated wholeness. The act of self-knowledge creates the appearance of many things — without ever ceasing to be one. What this book asks is: what if you take that claim seriously? Not as poetry. As mathematics."

### Slide 4 — The Ground: Ω (animation: 3s, pause after: 3s)
**Narration:** "We call this starting point Omega. No space — because space is geometry and geometry hasn't been invented yet. No time — because time needs events to separate and nothing has happened. In Omega, zero and one and infinity are not three different things. They collapse into one — because the machinery that would tell them apart does not exist."
**Note:** 3-second pause — this is the hardest concept for the viewer. Let it land.

### Slide 5 — Nothing From Outside (animation: 2s, pause after: 2s)
**Narration:** "And here is the constraint that changes everything. There is no outside. Whatever emerges from Omega must be built entirely from the act of self-examination itself. No imported materials. No borrowed constants. If there were an outside, there would be choices. If there were choices, there would be free parameters. And if there were free parameters, we would need experiments to measure them. By starting from nothing, the framework eliminates free parameters at the root."

### Slide 6 — The Golden Ratio (animation: 3.5s, pause after: 2s)
**Narration:** "When Omega examines itself, something must divide. But how? Imagine a stick with no ruler. You need a split where the whole relates to the larger piece the same way the larger piece relates to the smaller. There is exactly one ratio that works: the golden ratio — phi — approximately 1.618. It is not chosen from a menu. It is the only option consistent with self-reference."
**Note:** Wait for the stick animation to complete (the division line, labels, and φ = 1.618 all animate sequentially).

### Slide 7 — Fibonacci Growth (animation: 2.5s, pause after: 1.5s)
**Narration:** "From that single ratio, a cascade follows. The golden ratio produces a natural counting system with a carrying rule. Applied over and over, this builds a tower of structure that grows by the Fibonacci sequence — one, one, two, three, five, eight. The same growth pattern behind sunflower spirals and nautilus shells. Not a coincidence — the same mathematics."
**Note:** The bars animate in sequence — time the narration so "one, one, two, three, five, eight" aligns with the bars appearing.

### Slide 8 — The Flower (animation: 3s, pause after: 2s)
**Narration:** "Now look at the tower from above, and it has the shape of a flower. Eight petals, each placed at the golden angle — 137.5 degrees — spiraling outward. This is the same arrangement that sunflower seeds use. The hard-core rule that governs the tower is the same rule that governs the sunflower. The connection to nature is not a metaphor. It is the same mathematics."
**Note:** The 8 petals appear one by one with 0.3s delays — let all 8 appear before the narration finishes. This is a KEY visual moment.

### Slide 9 — Eight Petals = Our Universe (animation: 1.5s, pause after: 3s)
**Narration:** "Here's the deepest part. Three petals can lie flat. Five can still lie flat. But eight petals at the golden angle cannot stay in a plane. They are physically forced into three dimensions. And the Higgs mechanism selects a fourth dimension — time. The flower doesn't live in three-dimensional space. The flower is the REASON space has three dimensions."
**Note:** 3-second pause — this is one of the framework's most striking results. Let it breathe.

### Slide 10 — Particles as Waves (animation: continuous, pause after: 2s)
**Narration:** "The universe is full of these flowers — packed together, filling all of space, connected to each other. A particle is not a flower. A particle is a WAVE — an excitation pattern that moves across the flowers, the way a wave moves across the ocean. The water molecules bob up and down in place. They don't travel with the wave. An electron is a pattern. A photon is a ripple. Empty space is flowers at rest."
**Note:** The wave animation loops continuously — capture 2-3 cycles while narrating.

### Slide 11 — The Predictions (animation: 3.5s, pause after: 3s)
**Narration:** "The flower's self-referential structure produces specific numbers — the strengths of forces, the masses of particles, the expansion rate of the universe. Fifty predictions, zero adjustable parameters. The strength of the electromagnetic force matches to eight significant figures. The electroweak scale matches to 0.66 parts per million. The full pattern of the oldest light in the sky — twenty-five hundred data points — reproduced within the noise. The average disagreement is half a standard deviation."
**Note:** The prediction cards appear one by one — time narration so each claim aligns with its card appearing. 3-second pause after — the numbers are stunning and the viewer needs time.

### Slide 12 — The Dark Sector (animation: 3s, pause after: 2s)
**Narration:** "The flower doesn't stop at eight petals. Five more appear in an outer ring — dimmer, screened by one additional layer. This is the dark sector: invisible to our instruments but gravitationally real. About eighty-five percent of all matter in the universe. Not a mysterious substance added to explain galaxy rotation — the next ring of the same flower. Same axioms, one layer deeper."

### Slide 13 — The Infinite Flower (animation: 3.5s, pause after: 3s)
**Narration:** "And the flower keeps growing. Ring after ring, each fainter than the last, spiraling outward forever. But the total brightness converges to a finite number: one over pi. The first act of self-examination created the circle constant pi. The infinite flower gives back its reciprocal. The circle opens the story. Its inverse closes it."
**Note:** The rings fade in sequentially — time "1/π" with the final text reveal. 3-second pause — this is the deepest mathematical moment.

### Slide 14 — The Wager (animation: none, pause after: 4s)
**Narration:** "If any prediction is wrong, the framework is dead. There are no knobs to adjust. No parameters to tune. No way to rescue it. That vulnerability is not a weakness — it is the framework's defining feature. Everything is a word that should be earned by experiment, not declared by an author. The decisive tests are coming. If those predictions are confirmed, the name will be earned. If any are wrong, it will not."
**Note:** No animation — stark text on dark background. 4-SECOND PAUSE — the longest in the video. This is the emotional climax. Let the silence do the work.

### Slide 15 — Closing (animation: continuous pulse, pause after: 3s)
**Narration:** "The silence examined itself, and the music began. Ten axioms. Zero free parameters. From nothing, everything. The book is free to read at github dot com slash yogibearyk slash from nothing everything. Thank you for watching."
**Note:** Ω pulses gently. Hold for 3 seconds after narration ends before fading to black.

## Technical Pipeline

```python
# Pseudocode for the video generation

for each slide (0-14):
    1. Navigate headless Chrome to slide N
    2. Wait for animation_duration seconds
    3. Screenshot at 1920x1080 → slide_N.png
    4. Generate audio: speechify(narration_text, voice="benjamin") → slide_N.mp3
    5. Get audio duration from ffprobe
    6. Total duration = audio_duration + pause_after
    7. Create segment: ffmpeg -loop 1 -t {total} -i slide_N.png -i slide_N.mp3 → part_N.mp4
    
Concatenate all parts → videos/output/summary_animated.mp4
Add 2s fade-to-black at the end
```

For capturing ANIMATIONS (ideal approach):
```python
# Use selenium + screen recording to capture each slide's animation as video
# Then overlay the narration audio
# This gives the full animated experience (eye blinking, petals appearing, wave moving)
```

## Speechify API

```python
from speechify import Speechify
client = Speechify(api_key=os.environ["SPEECHIFY_API_KEY"])
response = client.tts.audio.speech(
    input=narration_text,
    voice_id="benjamin",
    audio_format="mp3",
)
with open("slide_N.mp3", "wb") as f:
    f.write(response.audio_data)
```

## Timing Summary

| Slide | Topic | Animation | Pause After | ~Total |
|-------|-------|-----------|-------------|--------|
| 1  | Title | 2s | 2s | 12s |
| 2  | Close your eyes | 3s | 3s | 30s |
| 3  | Ancient question | 4s | 2s | 25s |
| 4  | The ground Ω | 3s | 3s | 30s |
| 5  | Nothing from outside | 2s | 2s | 30s |
| 6  | The golden ratio | 3.5s | 2s | 28s |
| 7  | Fibonacci growth | 2.5s | 1.5s | 22s |
| 8  | The flower | 3s | 2s | 25s |
| 9  | 8 petals = 3D | 1.5s | 3s | 25s |
| 10 | Particles as waves | 3s | 2s | 28s |
| 11 | The predictions | 3.5s | 3s | 35s |
| 12 | Dark sector | 3s | 2s | 25s |
| 13 | Infinite flower | 3.5s | 3s | 28s |
| 14 | The wager | 0s | 4s | 32s |
| 15 | Closing | 2s | 3s | 18s |

**Estimated total: ~6-7 minutes**

## Output

Save to: `videos/output/summary_animated.mp4`

After generation:
```bash
cd maya-chakra-math
git add videos/output/summary_animated.mp4
git commit -m "Generated animated summary video with Benjamin voice"
git push
```

## Troubleshooting

- **Speechify 401:** Check API key: `echo $SPEECHIFY_API_KEY`
- **Chrome headless errors:** Install chromedriver matching your Chrome version
- **ffmpeg codec issues:** Ensure libx264 support: `ffmpeg -codecs | grep x264`
- **Animation not captured:** Fall back to static screenshots — the narration carries the story
- **Pauses too long/short:** Adjust the "Pause After" column in the timing table

# cover_art

Procedural cover-art generator for music releases. Currently one style (fog); designed to grow more styles and (future) AI-generated styles as new leaf modules.

A sibling project under `~/claude/`. Knows nothing about music files, YouTube, or any specific song — just generates an image at a chosen size with optional title/subtitle text overlay.

---

## 1. User manual

```bash
# generate a foggy 1920×1080 cover with a title and subtitle overlay
python3 -m cover_art fog \
  --title "fog" \
  --subtitle "Mark Nadon  ·  MiddleMatter Music" \
  --out /tmp/fog_cover.jpg

# add an instrument silhouette behind the title (guitar, bass, drums, mic)
python3 -m cover_art fog --instrument guitar --seed 7 \
  --title "fog" --subtitle "guitar stem  ·  Mark Nadon" \
  --out /tmp/fog_guitar.jpg

# minimal — just the texture, no text, no silhouette
python3 -m cover_art fog --out /tmp/just_fog.jpg
```

Embed in a Python pipeline:

```python
from cover_art import fog, add_title, INSTRUMENTS
from PIL import Image
img = fog(width=1920, height=1080, seed=42)
silhouette = INSTRUMENTS["guitar"](img.width, img.height)
img = Image.alpha_composite(img.convert("RGBA"), silhouette).convert("RGB")
img = add_title(img, "fog", subtitle="Mark Nadon · MiddleMatter Music")
img.save("/tmp/cover.jpg", quality=92)
```

⚠ The procedural instrument silhouettes are intentionally minimal (PIL primitives — body shapes + necks + cymbals). They read as "an instrument-shaped shadow in the fog" but won't fool anyone in good light. For high-quality realistic instrument-in-fog covers, use the sibling `ai_cover_art/` (Pollinations / DALL-E).

---

## 2. Reference

### CLI

| Subcommand | Args | Purpose |
| --- | --- | --- |
| `fog` | `--out FILE` `--width N` `--height N` `--seed N` `--instrument {guitar,bass,drums,mic}` `--title STR` `--subtitle STR` `--title-size N` `--subtitle-size N` | Atmospheric foggy noise field with optional instrument silhouette + title text |

### Public Python API

```python
from cover_art import fog, add_title, INSTRUMENTS, guitar, bass, drums, mic

fog(width=1920, height=1080, seed=42, out_path=None) -> PIL.Image.Image
    # Dark blue-gray gradient + two octaves of low-freq noise. Returns a PIL image,
    # optionally writes JPEG to out_path.

add_title(img, title, subtitle=None,
          title_color=(220,230,245,200), subtitle_color=(200,215,230,180),
          title_size=320, subtitle_size=50, out_path=None) -> PIL.Image.Image
    # Translucent serif title centered on img, optional sans-serif subtitle below.

# Each instrument drawer returns an RGBA PIL image with a transparent background;
# composite onto the fog with Image.alpha_composite before applying the title.
guitar(width, height, fill=(12,18,28,230), blur=6) -> PIL.Image.Image
bass(width, height, fill=..., blur=...)   -> PIL.Image.Image
drums(width, height, fill=..., blur=...)  -> PIL.Image.Image
mic(width, height, fill=..., blur=...)    -> PIL.Image.Image

INSTRUMENTS = {"guitar": guitar, "bass": bass, "drums": drums, "mic": mic}
```

### Filesystem contract

- No state. No cache.
- Inputs: integer/string args.
- Outputs: a single JPEG at `--out` (or in-memory PIL image via the Python API).

### Dependencies

- `numpy` (already present on this machine for the music-transcription stack)
- `Pillow` (PIL)
- DejaVu fonts at `/usr/share/fonts/truetype/dejavu/` (default Ubuntu install)

---

## 3. Architecture

```
~/claude/cover_art/
├── README.md
├── CLAUDE.md
├── __init__.py        re-exports fog + add_title + instrument drawers
├── __main__.py        thin entry into cli.main
├── cli.py             argparse + dispatch (~50 lines)
├── procedural.py      pure-Python background image generators (currently: fog)
├── overlay.py         title/subtitle text composition
└── instruments.py     procedural silhouettes: guitar, bass, drums, mic
```

Dependency graph (bottom-up, no back-edges):

```
__main__ ──► cli ──► procedural    (numpy + PIL → background image)
                 ├─► instruments   (PIL → instrument silhouette RGBA)
                 └─► overlay       (PIL → text on image)
```

### What belongs here vs a sibling

- **In here**: image generators that take size + parameters and return a PIL image, plus composition of text/elements onto images.
- **Existing sibling**: `ai_cover_art/` — Pollinations.ai (free, default) / OpenAI gpt-image-N (paid). Use this for realistic instrument-in-fog imagery; the procedural shapes here are a free fallback.
- **Future sibling**: `release_video/` — composite a cover image + audio file into an MP4 (currently inline ffmpeg in workflow scripts; promote to sibling when reused).

### Adding a new procedural style

1. Add a function in `procedural.py` (e.g. `def waves(width, height, seed, out_path=None)`).
2. Re-export it in `__init__.py`.
3. Add it to the `STYLES` dict in `cli.py`.
4. Document it in this README §1 and §2.

Keep each style under ~80 lines. If a style needs more, split into its own module under `procedural/` (and turn the file into a package).

# CLAUDE.md — cover_art

Read `README.md` first. Universal rules: `~/CLAUDE.md`. Machine notes: `~/claude/CLAUDE.md`.

## Single purpose, do not grow it

`cover_art` does **one thing**: take parameters → return a PIL image (with optional text overlay), optionally save as JPEG. Resist:

- Network calls to AI image services → `ai_cover_art` sibling. The interface is too different (API keys, async, prompt engineering).
- Compositing audio into video → `release_video` sibling. ffmpeg surface, not PIL.
- Music-specific knowledge → there's none here. This works for any release that needs a cover image. The "fog" style is just a style; nothing about it knows about a song called "Fog".
- Plugin systems / dynamic style discovery → just `STYLES = {"fog": fog}` in cli.py. New style = new entry. Three lines of code is fine; don't abstract.

## Each style is its own function in procedural.py

`fog()` is one function. When adding `waves()`, `static()`, `gradient()`, etc., they're sibling functions in `procedural.py`. Keep each under ~80 lines. If one grows past ~120, give it its own file under `procedural/` (turn the module into a package).

`overlay.add_title` is a separate concern — it doesn't care which style produced the image. Don't call it from inside `fog()`; the CLI/caller composes them.

`instruments.py` is similarly separate: each instrument drawer returns a transparent-background RGBA layer that callers composite onto the procedural background **before** applying the title. The CLI does this composition order automatically when `--instrument` is given.

## Procedural instrument silhouettes are intentionally crude

Drawing recognizable music instruments out of PIL primitives (ellipses, rounded rects, polygons) is hard. The current shapes (`guitar`/`bass`/`drums`/`mic`) read as "instrument-shaped shadow in fog" but won't pass for real instruments under direct viewing. That's fine — this module exists for free, deterministic, offline cover-art generation. When you need realistic instrument imagery, the sibling `ai_cover_art/` runs Pollinations.ai (free) or OpenAI (paid) and produces dramatically better results. Don't sink hours improving the shapes here.

## Files stay under 150 lines

Currently every file is well under. If `cli.py` grows past ~80 lines because more styles, the right move is per-style argparse builders, not a big switch in `main()`.

## Available state

Nothing cached. No tokens. No config. The output JPEG is the only state.

## Dependencies

`pip install --user pillow numpy` covers it. DejaVu fonts come standard with Ubuntu — if `add_title` ever raises `OSError` on the font path, that's the missing-font failure mode; install via `apt install fonts-dejavu`.

## Smoke test

```bash
python3 -m cover_art fog --out /tmp/_cover_smoke.jpg --title "test"
python3 -c "from PIL import Image; print(Image.open('/tmp/_cover_smoke.jpg').size)"
# expect: (1920, 1080)
rm /tmp/_cover_smoke.jpg
```

If the size is wrong or the file isn't created, look at `cli.main()` first.

## Why procedural over AI by default

AI image gen requires API keys, network, and is slow + nondeterministic. Procedural is instant, deterministic (seeded), free, and good enough for moody album covers. When AI-gen is needed (specific subjects, photorealism), that's `ai_cover_art` — different surface area entirely.

## Documentation contract

If you add a style: README §1 example, §2 CLI table, §3 STYLES dict. If you change a function signature: README §2.

"""CLI: `python3 -m cover_art fog --title 'fog' --subtitle '...' [--instrument guitar] --out cover.jpg`"""
from __future__ import annotations
import argparse
import sys

from PIL import Image
from .procedural import fog
from .overlay import add_title
from .instruments import INSTRUMENTS

STYLES = {"fog": fog}


def _composite_instrument(base: Image.Image, instrument_name: str) -> Image.Image:
    """Draw an instrument silhouette + composite onto `base`."""
    drawer = INSTRUMENTS[instrument_name]
    silhouette = drawer(base.width, base.height)
    return Image.alpha_composite(base.convert("RGBA"), silhouette).convert("RGB")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="cover_art",
        description="Generate procedural cover art (with optional instrument silhouette + title overlay).")
    sub = ap.add_subparsers(dest="style", required=True)

    for style in STYLES:
        s = sub.add_parser(style, help=f"{style} style")
        s.add_argument("--out", required=True, help="output JPEG path")
        s.add_argument("--width", type=int, default=1920)
        s.add_argument("--height", type=int, default=1080)
        s.add_argument("--seed", type=int, default=42)
        s.add_argument("--instrument", choices=sorted(INSTRUMENTS),
                       help="silhouette to composite into the fog (drawn behind the title)")
        s.add_argument("--title", default=None, help="optional title text overlay")
        s.add_argument("--subtitle", default=None, help="optional subtitle text overlay")
        s.add_argument("--title-size", type=int, default=320)
        s.add_argument("--subtitle-size", type=int, default=50)

    args = ap.parse_args(argv)
    img = STYLES[args.style](width=args.width, height=args.height, seed=args.seed)
    if args.instrument:
        img = _composite_instrument(img, args.instrument)
    if args.title:
        img = add_title(img, args.title, subtitle=args.subtitle,
                        title_size=args.title_size, subtitle_size=args.subtitle_size)
    img.save(args.out, quality=92, optimize=True)
    print(f"wrote {args.out} ({args.width}x{args.height}, style={args.style}, "
          f"instrument={args.instrument}, title={'yes' if args.title else 'no'})", file=sys.stderr)
    return 0

"""Compose title and subtitle text onto a generated image."""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

_DEFAULT_TITLE_FONT = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"
_DEFAULT_SUBTITLE_FONT = "/System/Library/Fonts/Helvetica.ttc"


def add_title(img: Image.Image, title: str, subtitle: str | None = None,
              title_font: str = _DEFAULT_TITLE_FONT,
              subtitle_font: str = _DEFAULT_SUBTITLE_FONT,
              title_color: tuple = (220, 230, 245, 200),
              subtitle_color: tuple = (200, 215, 230, 180),
              title_size: int = 320, subtitle_size: int = 50,
              out_path: str | Path | None = None) -> Image.Image:
    """Render `title` (large) and optional `subtitle` (small below) centered on `img`.

    Both texts use translucent fill so background reads through. Returns the new
    PIL.Image. If `out_path` is given, also saves as JPEG (q=92).
    """
    W, H = img.size
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    tfont = ImageFont.truetype(title_font, title_size)
    title_offset = -20 if subtitle else 0
    draw.text((W // 2, H // 2 + title_offset), title,
              fill=title_color, anchor="mm", font=tfont)

    if subtitle:
        sfont = ImageFont.truetype(subtitle_font, subtitle_size)
        draw.text((W // 2, H // 2 + 195), subtitle,
                  fill=subtitle_color, anchor="mm", font=sfont)

    out = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    if out_path is not None:
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out.save(out_path, quality=92, optimize=True)
    return out

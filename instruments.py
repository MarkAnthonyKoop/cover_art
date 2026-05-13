"""Procedural silhouettes of musical instruments, for compositing into cover art.

Each function draws onto a transparent RGBA canvas at the requested size and
returns the PIL image. The shapes are intentionally simple — meant to be blurred
and composited at moderate opacity so they read as "instrument-shaped shadow in
the fog" rather than detailed illustrations.
"""
from __future__ import annotations
from PIL import Image, ImageDraw, ImageFilter

# The compositing color is a slightly-darker-than-fog blue-gray. Caller can
# adjust by passing a different `fill`.
_DEFAULT_FILL = (12, 18, 28, 230)
_DEFAULT_BLUR = 6


def _finalize(canvas: Image.Image, blur: float) -> Image.Image:
    return canvas.filter(ImageFilter.GaussianBlur(radius=blur))


def guitar(width: int, height: int, fill: tuple = _DEFAULT_FILL,
           blur: float = _DEFAULT_BLUR) -> Image.Image:
    """Acoustic guitar dreadnought silhouette, body lower, neck up-right."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = width // 2, int(height * 0.62)
    bw = int(min(width, height) * 0.45)        # body width
    # Lower bout (bigger)
    d.ellipse([cx - bw // 2, cy - int(bw * 0.35),
               cx + bw // 2, cy + int(bw * 0.55)], fill=fill)
    # Upper bout (smaller, overlapping above)
    ub = int(bw * 0.78)
    d.ellipse([cx - ub // 2, cy - int(bw * 0.85),
               cx + ub // 2, cy - int(bw * 0.05)], fill=fill)
    # Sound hole (cut-out — paint with the canvas's transparent color)
    sh = int(bw * 0.18)
    d.ellipse([cx - sh, cy - sh, cx + sh, cy + sh], fill=(0, 0, 0, 0))
    # Neck up and slightly right
    nw = int(bw * 0.10)
    nl = int(height * 0.55)
    d.polygon([(cx - nw // 2, cy - int(bw * 0.55)),
               (cx + nw // 2, cy - int(bw * 0.55)),
               (cx + nw // 2 + int(nl * 0.05), cy - int(bw * 0.55) - nl),
               (cx - nw // 2 + int(nl * 0.05), cy - int(bw * 0.55) - nl)], fill=fill)
    # Headstock
    hw = int(nw * 1.6)
    hy = cy - int(bw * 0.55) - nl
    d.polygon([(cx + int(nl * 0.05) - hw // 2, hy),
               (cx + int(nl * 0.05) + hw // 2, hy),
               (cx + int(nl * 0.05) + hw // 2 - 4, hy - int(hw * 1.3)),
               (cx + int(nl * 0.05) - hw // 2 + 4, hy - int(hw * 1.3))], fill=fill)
    return _finalize(img, blur)


def bass(width: int, height: int, fill: tuple = _DEFAULT_FILL,
         blur: float = _DEFAULT_BLUR) -> Image.Image:
    """Electric bass: solid body (no sound hole), long neck."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = width // 2, int(height * 0.70)
    bw = int(min(width, height) * 0.40)
    # P-bass body: rounded with double cutaway hint
    d.rounded_rectangle([cx - bw // 2, cy - int(bw * 0.32),
                         cx + bw // 2, cy + int(bw * 0.48)],
                        radius=int(bw * 0.30), fill=fill)
    # Long neck up
    nw = int(bw * 0.09)
    nl = int(height * 0.62)
    d.rectangle([cx - nw // 2, cy - int(bw * 0.32) - nl,
                 cx + nw // 2, cy - int(bw * 0.32)], fill=fill)
    # Headstock (sideways P-style)
    hw, hh = int(nw * 4.0), int(nw * 1.6)
    hy = cy - int(bw * 0.32) - nl
    d.polygon([(cx - nw // 2, hy),
               (cx + nw // 2, hy),
               (cx + nw // 2 + hw, hy - hh // 2),
               (cx + nw // 2 + hw, hy - hh),
               (cx - nw // 2, hy - hh)], fill=fill)
    return _finalize(img, blur)


def drums(width: int, height: int, fill: tuple = _DEFAULT_FILL,
          blur: float = _DEFAULT_BLUR) -> Image.Image:
    """Drum kit silhouette: kick (front), snare (in front of kick), two cymbals."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = width // 2, int(height * 0.65)
    s = int(min(width, height) * 0.42)         # kit "size" reference
    # Kick drum (head-on ellipse, dominant)
    d.ellipse([cx - s, cy - s // 2, cx + s, cy + s], fill=fill)
    # Snare drum in front, smaller, lower
    sn = int(s * 0.45)
    d.ellipse([cx - sn // 2 - sn, cy + int(s * 0.55),
               cx - sn // 2, cy + int(s * 0.55) + sn // 2], fill=fill)
    # Cymbals (two ovals tilted, behind the kick)
    cym_w, cym_h = int(s * 0.85), int(s * 0.10)
    # left cymbal stand (vertical line)
    d.rectangle([cx - s + 30, cy - s, cx - s + 38, cy - s + cym_h], fill=fill)
    d.ellipse([cx - s - cym_w // 2 + 30, cy - s,
               cx - s + cym_w // 2 + 30, cy - s + cym_h], fill=fill)
    # right cymbal
    d.rectangle([cx + s - 38, cy - s, cx + s - 30, cy - s + cym_h], fill=fill)
    d.ellipse([cx + s - cym_w // 2 - 30, cy - s,
               cx + s + cym_w // 2 - 30, cy - s + cym_h], fill=fill)
    return _finalize(img, blur)


def mic(width: int, height: int, fill: tuple = _DEFAULT_FILL,
        blur: float = _DEFAULT_BLUR) -> Image.Image:
    """Vocal mic on a boom stand."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = width // 2
    head_r = int(min(width, height) * 0.10)
    head_y = int(height * 0.45)
    # Mic head (capsule/grille)
    d.ellipse([cx - head_r, head_y - head_r,
               cx + head_r, head_y + head_r], fill=fill)
    # Mic body (cylinder below grille)
    body_w = int(head_r * 0.65)
    body_h = int(head_r * 1.6)
    d.rounded_rectangle([cx - body_w // 2, head_y + head_r - 4,
                         cx + body_w // 2, head_y + head_r + body_h],
                        radius=8, fill=fill)
    # Boom arm (diagonal up-left from base) and stand (vertical from below)
    base_x = cx - int(head_r * 4)
    base_y = int(height * 0.92)
    d.polygon([(cx, head_y + head_r + body_h),
               (cx + 12, head_y + head_r + body_h + 12),
               (base_x + 12, base_y - int(head_r * 4)),
               (base_x, base_y - int(head_r * 4) - 12)], fill=fill)
    d.rectangle([base_x - 6, base_y - int(head_r * 4),
                 base_x + 14, base_y], fill=fill)
    # Floor base (oval)
    d.ellipse([base_x - int(head_r * 1.2), base_y - 10,
               base_x + int(head_r * 1.2), base_y + 18], fill=fill)
    return _finalize(img, blur)


INSTRUMENTS = {"guitar": guitar, "bass": bass, "drums": drums, "mic": mic}

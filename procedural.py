"""Procedural cover-art generators: pure-Python images with no external models.

Currently one style: fog (atmospheric blue-gray noise field). Add new styles as
sibling functions in this module — keep each under ~80 lines.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter


def _fog_layer(width: int, height: int, scale: int, blur: int,
               contrast: float, seed: int) -> np.ndarray:
    """One octave of low-freq noise → upsample → blur → returns float32 [0..255]."""
    rng = np.random.RandomState(seed)
    small = rng.randn(height // scale, width // scale).astype(np.float32) * contrast
    img = Image.fromarray(((small + 128).clip(0, 255)).astype(np.uint8))
    img = img.resize((width, height), Image.BICUBIC)
    img = img.filter(ImageFilter.GaussianBlur(radius=blur))
    return np.array(img, dtype=np.float32)


def fog(width: int = 1920, height: int = 1080, seed: int = 42,
        out_path: str | Path | None = None) -> Image.Image:
    """Generate an atmospheric foggy image: dark blue-gray gradient + 2 noise octaves.

    Returns the PIL.Image. If `out_path` is given, also saves as JPEG (q=92).
    """
    gradient = np.linspace(28, 58, height).reshape(-1, 1).astype(np.float32)
    base = np.zeros((height, width, 3), dtype=np.float32)
    base[..., 0] = gradient * 0.85           # R
    base[..., 1] = gradient * 0.95           # G
    base[..., 2] = gradient * 1.10 + 12      # B (cool tint)

    big   = _fog_layer(width, height, scale=24, blur=60, contrast=80, seed=seed)
    small = _fog_layer(width, height, scale=8,  blur=22, contrast=50, seed=seed + 1)

    def lighten(rgb: np.ndarray, gray: np.ndarray, weight: float) -> np.ndarray:
        add = np.stack([gray * 0.95, gray * 1.00, gray * 1.05], axis=-1) * weight
        return np.clip(rgb + add, 0, 255)

    arr = lighten(base, big,   weight=0.55)
    arr = lighten(arr,  small, weight=0.30)
    img = Image.fromarray(arr.astype(np.uint8))

    if out_path is not None:
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(out_path, quality=92, optimize=True)
    return img

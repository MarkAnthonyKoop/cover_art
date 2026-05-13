"""cover_art — procedural and (future) AI-generated cover images for music releases."""
from .procedural import fog
from .overlay import add_title
from .instruments import INSTRUMENTS, guitar, bass, drums, mic

__all__ = ["fog", "add_title", "INSTRUMENTS", "guitar", "bass", "drums", "mic"]

"""Smoke test for cover_art — verifies the package imports cleanly."""
import importlib


def test_import():
    mod = importlib.import_module("cover_art")
    assert mod is not None


def test_main_module_importable():
    # `python3 -m cover_art` works iff this import works
    importlib.import_module("cover_art.__main__")

"""Render Recorded Lectures with the shared Joy menu system."""
import sys
from pathlib import Path


def render(data):
    menus = Path(__file__).resolve().parent.parent / "menus"
    if str(menus) not in sys.path:
        sys.path.insert(0, str(menus))
    from build_menu import build

    data = dict(data)
    course = dict(data["course"])
    course["dataFile"] = "recorded-lectures.json"
    data["course"] = course
    return build(data)

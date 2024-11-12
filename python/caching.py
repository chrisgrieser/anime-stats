"""Simple, generic caching mechanism."""

from __future__ import annotations

import json
from pathlib import Path

CACHE_PATH = "./cache"


def read(cachename: str) -> dict[str, object]:
    """Read the cache file."""
    path = Path(CACHE_PATH + "/" + cachename)
    if path.exists():
        with path.open("r") as f:
            cache: dict[str, object] = json.load(f)
    else:
        cache = {}
    return cache


def write(cachename: str, cache: dict[str, object]) -> None:
    """Write the cache file."""
    path = Path(CACHE_PATH + "/" + cachename)
    Path.mkdir(path.parent, exist_ok=True)
    with path.open("w") as f:
        json.dump(cache, f)

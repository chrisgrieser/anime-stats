"""Simple, generic caching mechanism."""

from __future__ import annotations

import json
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────

CACHE_PATH = "./cache"

# ──────────────────────────────────────────────────────────────────────────────


def read_json(cache_name: str) -> dict[str, object]:
    """Read the cache file."""
    if cache_name.endswith(".json"):
        cache_name = cache_name[:-5]
    path = Path(CACHE_PATH + "/" + cache_name + ".json")

    if path.exists():
        with path.open("r") as f:
            cache: dict[str, object] = json.load(f)
    else:
        cache = {}
    return cache


def write_json(cache_name: str, cache: dict[str, object]) -> None:
    """Write the cache file."""
    if cache_name.endswith(".json"):
        cache_name = cache_name[:-5]
    path = Path(CACHE_PATH + "/" + cache_name + ".json")

    Path.mkdir(path.parent, exist_ok=True)
    with path.open("w") as f:
        json.dump(cache, f)

"""Simple, generic caching mechanism."""

from __future__ import annotations

import json
from pathlib import Path

# CONFIG
cache_path = "./cache/api_cache.json"

# ──────────────────────────────────────────────────────────────────────────────


def read() -> dict[str, object]:
    """Read the cache file."""
    if Path(cache_path).exists():
        with Path(cache_path).open("r") as f:
            api_cache: dict[str, object] = json.load(f)
    else:
        api_cache = {}
    return api_cache


def write(api_cache: dict[str, object]) -> None:
    """Write the cache file."""
    Path.mkdir(Path(cache_path).parent, exist_ok=True)
    with Path(cache_path).open("w") as f:
        json.dump(api_cache, f)

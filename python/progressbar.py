"""Simple progress bar for the terminal."""

from typing import TypedDict

CHARS = {
    "empty": "─",
    "load": "■",
    "load_from_cache": "□",
}


class BarState(TypedDict):
    """Simple state management for the progress bar."""

    bar_len: int  # total length the bar will have
    previous: str  # previously printed chars


state: BarState = {
    "bar_len": 0,
    "previous": "",
}

# ──────────────────────────────────────────────────────────────────────────────


def init(length: int) -> None:
    """Define the length of the progress bar."""
    state["bar_len"] = length


def increment(*, from_cache: bool = False) -> None:
    """Simple progress bar.

    Use `from_cache=True` to use an alternate char.
    """
    bar = state["previous"] + (CHARS["load"] if not from_cache else CHARS["load_from_cache"])
    filled_bar = bar + (state["bar_len"] - len(bar)) * CHARS["empty"]
    # `\33[2K` = full line erasure, `\r` = move cursor to start
    print("\33[2K\r" + filled_bar, end="", flush=True)
    state["previous"] = bar


def remove() -> None:
    """Remove the progress bar and reset the state."""
    print("\33[2K\r", end="", flush=True)
    state["previous"] = ""
    state["bar_len"] = 0

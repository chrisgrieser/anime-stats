"""Simple progress bar for the temrinal."""

EMPTY_CHAR = "─"
CHAR = "■"
FROM_CACHE = "□"


progressbar_len = 0
previous_progress = ""

# ──────────────────────────────────────────────────────────────────────────────


def init(length: int) -> None:
    """Define the length of the progress bar."""
    global progressbar_len  # noqa: PLW0603
    progressbar_len = length


def increment(*, from_cache: bool = False) -> None:
    """Simple progress bar.

    Use `from_cache=True` to use an alternate char.
    """
    global previous_progress  # noqa: PLW0603
    previous_progress += CHAR if not from_cache else FROM_CACHE
    filled_bar = previous_progress + (progressbar_len - len(previous_progress)) * EMPTY_CHAR
    print("\r" + filled_bar, end="", flush=True)


def remove() -> None:
    """Remove the progress bar."""
    print("\r" + " " * 100 + "\r", end="", flush=True)

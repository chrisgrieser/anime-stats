"""Docstring."""

from __future__ import annotations

import sys
import time

import requests

# ──────────────────────────────────────────────────────────────────────────────

# CONFIG
start_year = 2020
end_year = 2024
base_api = "https://api.jikan.moe/v4"


# ──────────────────────────────────────────────────────────────────────────────

# INFO rate limit 3/s, 60/min https://docs.api.jikan.moe/#section/Information/Rate-Limiting
request_count = 0
calls_per_second = 3


def wait_for_api_rate_limit() -> None:
    """Wait for api rate limit."""
    global request_count  # noqa: PLW0603 okay here
    request_count += 1
    if request_count > calls_per_second:
        print("Rate limit reached, waiting 1 second…")
        request_count = 0
        time.sleep(1.5)


# ──────────────────────────────────────────────────────────────────────────────


def get_shows_per_year() -> dict[int, int]:
    """Execute main function."""
    shows_per_year: dict[int, int] = {}

    # DOCS request https://docs.api.jikan.moe/#tag/anime/operation/getAnimeSearch
    for year in range(start_year, end_year + 1):
        wait_for_api_rate_limit()
        api_url = f"{base_api}/anime?start_date={year}-01-01&end_date={year}-12-31&type=tv"
        response = requests.get(api_url, timeout=10)
        http_status_success = 200
        if response.status_code != http_status_success:
            print("Error:", response.status_code, response.reason)
            sys.exit(1)

        pagination = response.json()["pagination"]  # pyright: ignore [reportAny]
        shows_per_year[year] = pagination["items"]["total"]

    return shows_per_year


# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    out = get_shows_per_year()
    print(f"🖨️ {out = }")

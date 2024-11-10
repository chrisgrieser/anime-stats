"""Docstring."""

from __future__ import annotations

import sys
import time
from typing import TypedDict

import requests

# ──────────────────────────────────────────────────────────────────────────────

# CONFIG
start_year = 2020
end_year = 2024
base_api = "https://api.jikan.moe/v4"


# ──────────────────────────────────────────────────────────────────────────────

request_count = 0  # share for all api calls


def wait_for_api_rate_limit() -> None:
    """Wait for api rate limit."""
    calls_per_second = 3 # https://docs.api.jikan.moe/#section/Information/Rate-Limiting
    global request_count  # noqa: PLW0603 too convoluted without `global`
    request_count += 1
    if request_count > calls_per_second:
        request_count = 0
        time.sleep(1.5)


class YearData(TypedDict):
    """Data for a year."""

    total: int
    isekais: int


# ──────────────────────────────────────────────────────────────────────────────


def get_data_per_year() -> dict[int, YearData]:
    """Get the total number of shows per year.

    DOCS https://docs.api.jikan.moe/#tag/anime/operation/getAnimeSearch
    """
    year_data: dict[int, YearData] = {}

    for year in range(start_year, end_year + 1):
        wait_for_api_rate_limit()
        api_url = f"{base_api}/anime?start_date={year}-01-01&end_date={year}-12-31&type=tv"
        response = requests.get(api_url, timeout=10)
        http_status_success = 200
        if response.status_code != http_status_success:
            print("Error:", response.status_code, response.reason)
            sys.exit(1)

        pagination = response.json()["pagination"]  # pyright: ignore [reportAny]
        if year not in year_data:
            year_data[year] = {"total": 0, "isekais": 0}

        year_data[year]["total"] = pagination["items"]["total"]

    return year_data


# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    year_data = get_data_per_year()

    to_print = ""
    for year, data in year_data.items():
        to_print += f"{year}: {data["total"]}\n"
    print(to_print)

"""Docstring."""

from __future__ import annotations

import sys
from time import sleep
from typing import TypedDict

import requests

# ──────────────────────────────────────────────────────────────────────────────

# CONFIG
start_year = 2014
end_year = 2024
genre_id = 35  # 62 = isekai, see https://api.jikan.moe/v4/genres/anime
genre_name = "Romance"
genre_exclude_id = 4
genre_exclude_name = "Comedy"

# ──────────────────────────────────────────────────────────────────────────────

call_count = 0


def make_jikan_api_call(url: str) -> object:
    """Make a jikan api call."""
    # wait for rate limit, 3 calls per second https://docs.api.jikan.moe/#section/Information/Rate-Limiting
    sleep(1)

    # simple progress bar
    global call_count  # noqa: PLW0603
    call_count += 1
    _ = sys.stdout.write("\r")
    _ = sys.stdout.write("▱" * call_count)
    _ = sys.stdout.flush()

    # make request
    response = requests.get(url, timeout=10)
    http_status_success = 200
    if response.status_code != http_status_success:
        print("Error:", response.status_code, response.reason)
        sys.exit(1)
    return response.json()  # pyright: ignore [reportAny]


class YearData(TypedDict):
    """Data for a year."""

    total: int
    of_genre: int


# ──────────────────────────────────────────────────────────────────────────────


def get_data_per_year(genre_id: int) -> dict[int, YearData]:
    """Get the total number of shows per year.

    DOCS https://docs.api.jikan.moe/#tag/anime/operation/getAnimeSearch
    """
    year_data: dict[int, YearData] = {}

    for year in range(start_year, end_year + 1):
        base_api = "https://api.jikan.moe/v4"

        api_url = f"{base_api}/anime?start_date={year}-01-01&end_date={year}-12-31&type=tv"
        total_for_year = make_jikan_api_call(api_url)

        api_url += api_url + f"&genres={genre_id}"
        if genre_exclude_id:
            api_url += f"&exclude_genres={genre_exclude_id}"
        of_genre_for_year = make_jikan_api_call(api_url)

        year_data[year] = {
            "of_genre": of_genre_for_year["pagination"]["items"]["total"],  # pyright: ignore [reportIndexIssue]
            "total": total_for_year["pagination"]["items"]["total"],  # pyright: ignore [reportIndexIssue]
        }

    return year_data


# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    year_data = get_data_per_year(genre_id)

    header = [genre_name, "per year"]
    if genre_exclude_id:
        header.append(f"(excluding {genre_exclude_name})")
    to_print: list[str] = [" ".join(header).upper()]

    for year, data in year_data.items():
        of_genre, total = data["of_genre"], data["total"]
        share = round((of_genre / total) * 100)
        to_print.append(f"{year}: {of_genre}/{total} ({share}%)")

    print()
    print("\n".join(to_print))

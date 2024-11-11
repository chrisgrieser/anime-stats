"""Docstring."""

from __future__ import annotations

import json
from pathlib import Path
from sys import exit
from time import sleep
from typing import TypedDict

import requests

# ──────────────────────────────────────────────────────────────────────────────

# CONFIG
start_year = 2014
end_year = 2024
genre_id = 4  # 62 = isekai, see https://api.jikan.moe/v4/genres/anime
genre_name = "Comedy"

# disabled when set to falsy values
genre_exclude_id = 0
genre_exclude_name = ""

# ──────────────────────────────────────────────────────────────────────────────


def make_jikan_api_call(url: str, api_cache: dict[str, object]) -> tuple[object, dict[str, object]]:
    """Check cache, if API call is not in cache, make a jikan API call.

    Return the response and the updated cache.
    """
    # simple progress bar
    progress_char = "▰" if url in api_cache else "▱"
    print(progress_char, end="", flush=True)

    if url in api_cache:
        return api_cache[url], api_cache

    # wait for rate limit, 3 calls per second https://docs.api.jikan.moe/#section/Information/Rate-Limiting
    sleep(0.8)

    # make request
    response = requests.get(url, timeout=10)
    http_status_success = 200
    if response.status_code != http_status_success:
        print("Error:", response.status_code, response.reason)
        exit(1)

    api_cache[url] = response.json()
    return response.json(), api_cache


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
        cache = "./cache/api_cache.json"

        # cache
        if Path(cache).exists():
            with Path(cache).open("r") as f:
                api_cache: dict[str, object] = json.load(f)
        else:
            api_cache = {}

        # make API calls
        api_url = f"{base_api}/anime?start_date={year}-01-01&end_date={year}-12-31&type=tv"
        total_for_year, api_cache = make_jikan_api_call(api_url, api_cache)

        api_url += api_url + f"&genres={genre_id}"
        if genre_exclude_id:
            api_url += f"&genres_exclude={genre_exclude_id}"
        of_genre_for_year, api_cache = make_jikan_api_call(api_url, api_cache)

        year_data[year] = {
            "of_genre": of_genre_for_year["pagination"]["items"]["total"],  # pyright: ignore [reportIndexIssue]
            "total": total_for_year["pagination"]["items"]["total"],  # pyright: ignore [reportIndexIssue]
        }

        # write cache
        Path.mkdir(Path(cache).parent, exist_ok=True)
        with Path(cache).open("w") as f:
            json.dump(api_cache, f)

    return year_data


def print_result(year_data: dict[int, YearData]) -> None:
    """Remove the progress bar and print the result."""
    header = [genre_name, "per year"]
    if genre_exclude_id:
        header.append(f"(excluding {genre_exclude_name})")
    to_print: list[str] = [" ".join(header)]

    for year, data in year_data.items():
        of_genre, total = data["of_genre"], data["total"]
        share = round((of_genre / total) * 100)
        to_print.append(f"{year}: {of_genre}/{total} ({share}%)")

    # remove progress bar
    print("\r", end="")
    print(" " * len(to_print * 2), end="")
    print("\r", flush=True, end="")

    print("\n".join(to_print))


# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    year_data = get_data_per_year(genre_id)
    print_result(year_data)

"""Docstring."""

from __future__ import annotations

import datetime
import sys
from time import sleep
from typing import TypedDict

import matplotlib.pyplot as plt
import requests

from . import caching

# ──────────────────────────────────────────────────────────────────────────────

# CONFIG excluded genres
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
    sleep(0.65)

    # make request
    response = requests.get(url, timeout=10)
    http_status_success = 200
    if response.status_code != http_status_success:
        print("\r", flush=True, end="")
        print("Error:", response.status_code, response.reason)
        sys.exit(1)

    api_cache[url] = response.json()
    return response.json(), api_cache


class YearData(TypedDict):
    """Data for a year."""

    total: int
    of_genre: int
    percent: float


# ──────────────────────────────────────────────────────────────────────────────


def get_data_per_year(genre_name: str, start_year: int) -> dict[int, YearData]:
    """Get the total number of shows per year.

    DOCS https://docs.api.jikan.moe/#tag/anime/operation/getAnimeSearch
    """
    end_year = datetime.datetime.now(tz=datetime.UTC).year  # current year
    genre_id = get_genre_id(genre_name)

    year_data: dict[int, YearData] = {}

    for year in range(start_year, end_year + 1):
        base_api = "https://api.jikan.moe/v4"
        api_cache = caching.read()

        api_url = f"{base_api}/anime?start_date={year}-01-01&end_date={year}-12-31&type=tv"
        total_for_year, api_cache = make_jikan_api_call(api_url, api_cache)

        api_url += api_url + f"&genres={genre_id}"
        if genre_exclude_id:
            api_url += f"&genres_exclude={genre_exclude_id}"
        of_genre_for_year, api_cache = make_jikan_api_call(api_url, api_cache)

        of_genre: int = of_genre_for_year["pagination"]["items"]["total"]  # pyright: ignore [reportIndexIssue,reportUnknownVariableType]
        total: int = total_for_year["pagination"]["items"]["total"]  # pyright: ignore [reportIndexIssue,reportUnknownVariableType]

        year_data[year] = {
            "of_genre": of_genre,
            "total": total,
            "percent": round(of_genre / total * 100),  # pyright: ignore [reportUnknownArgumentType]
        }

        caching.write(api_cache)

    return year_data


def get_genre_id(genre_name: str) -> int:
    """Get MAL genre id from genre name (case insensitive).

    https://docs.api.jikan.moe/#tag/genres/operation/getAnimeGenres
    """
    cache = caching.read()
    genre_data, api_cache = make_jikan_api_call("https://api.jikan.moe/v4/genres/anime", cache)
    genre: int | None = next(  # pyright: ignore [reportUnknownVariableType]
        (
            el
            for el in genre_data["data"]  # pyright: ignore [reportIndexIssue,reportUnknownArgumentType,reportUnknownVariableType]
            if el["name"].lower() == genre_name.lower()
        ),
        None,
    )
    if not genre:
        print("\r", flush=True, end="")
        print(f'Genre "{genre_name}" not found.')
        sys.exit(1)

    caching.write(api_cache)
    return genre["mal_id"]  # pyright: ignore [reportUnknownVariableType]


# ──────────────────────────────────────────────────────────────────────────────


def get_header(genre_name: str) -> str:
    """Get the header for the output."""
    header_parts = [f'"{genre_name}"', "per year"]
    if genre_exclude_id:
        header_parts.append(f"(excluding {genre_exclude_name})")
    return " ".join(header_parts)


def print_result_to_terminal(year_data: dict[int, YearData], header: str) -> None:
    """Remove the progress bar and print the result."""
    to_print: list[str] = [header]

    for year, data in year_data.items():
        of_genre, total, percent = data["of_genre"], data["total"], data["percent"]
        to_print.append(f"{year}: {of_genre}/{total} ({percent}%)")

    # remove progress bar
    print("\r", end="")
    print(" " * len(to_print * 2), end="")
    print("\r", flush=True, end="")

    print("\n".join(to_print))


def plot_results(year_data: dict[int, YearData], genre_name: str) -> None:
    """Plot the results via matplotlib."""
    years = list(year_data.keys())
    percentages = [data["percent"] for data in year_data.values()]

    # line plot
    plt.figure(figsize=(10, 6))
    plt.plot(years, percentages, marker="o", linestyle="-", color="b", label=genre_name)

    plt.title(get_header(genre_name))
    plt.xlabel("Year")
    plt.ylabel("Percent")

    plt.grid(visible=True)
    plt.legend()
    plt.show()


# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    genre_name, start_year = sys.argv[1], int(sys.argv[2])
    year_data = get_data_per_year(genre_name, start_year)
    header = get_header(genre_name)

    print_result_to_terminal(year_data, header)
    plot_results(year_data, genre_name)

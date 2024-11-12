"""Docstring."""

from __future__ import annotations

import datetime
import sys
from time import sleep

import requests

from . import caching, output, progressbar

# ──────────────────────────────────────────────────────────────────────────────


def make_jikan_api_call(url: str) -> dict[str, object]:
    """Make a jikan API call."""
    # wait for rate limit (3 per sec) https://docs.api.jikan.moe/#section/Information/Rate-Limiting
    sleep(0.8)

    response = requests.get(url, timeout=10)
    http_status_success = 200
    if response.status_code != http_status_success:
        print("\r", flush=True, end="")
        print("Error:", response.status_code, response.reason)
        sys.exit(1)

    json: dict[str, object] = response.json()
    return json


def get_data_per_year(genre_name: str, start_year: int) -> dict[str, object]:
    """Get the total number of shows per year.

    DOCS https://docs.api.jikan.moe/#tag/anime/operation/getAnimeSearch
    """
    end_year = datetime.datetime.now(tz=datetime.UTC).year  # current year
    year_range = range(start_year, end_year + 1)
    progressbar.init(len(year_range) * 2 + 1)  # 2 per year, +1 for genre

    genre_id = get_genre_id(genre_name)
    year_data = caching.read_json("year_data")

    for y in year_range:
        # init
        api_url = "https://api.jikan.moe/v4/anime?"
        year = str(y)  # using string keys for proper overwriting
        if year not in year_data:
            year_data[year] = {}

        # total
        api_url += f"start_date={year}-01-01&end_date={year}-12-31&type=tv"
        total: int
        if "total" in year_data[year]:  # pyright: ignore [reportOperatorIssue]
            progressbar.increment(from_cache=True)
            total = year_data[year]["total"]  # pyright: ignore [reportIndexIssue,reportUnknownVariableType]
        else:
            progressbar.increment()
            total = make_jikan_api_call(api_url)["pagination"]["items"]["total"]  # pyright: ignore [reportIndexIssue,reportUnknownVariableType]
            year_data[year]["total"] = total  # pyright: ignore [reportIndexIssue]

        # of genre
        api_url += api_url + f"&genres={genre_id}"
        of_genre: int
        if genre_name in year_data[year]:  # pyright: ignore [reportOperatorIssue]
            progressbar.increment(from_cache=True)
            of_genre = year_data[year][genre_name]  # pyright: ignore [reportIndexIssue,reportUnknownVariableType]
        else:
            progressbar.increment()
            of_genre = make_jikan_api_call(api_url)["pagination"]["items"]["total"]  # pyright: ignore [reportIndexIssue,reportUnknownVariableType]
            year_data[year][genre_name] = of_genre  # pyright: ignore [reportIndexIssue]
        year_data[year][genre_name + "_percent"] = round(of_genre / total * 100)  # pyright: ignore [reportUnknownArgumentType,reportIndexIssue]

    year_data = dict(sorted(year_data.items()))  # sorting in case of caching
    caching.write_json("year_data.json", year_data)

    return year_data


def get_genre_id(genre_name: str) -> int:
    """Get MAL genre id from genre name (case insensitive).

    https://docs.api.jikan.moe/#tag/genres/operation/getAnimeGenres
    """
    genre_data = caching.read_json("genres")
    if len(genre_data) == 0:
        progressbar.increment()
        genre_data = make_jikan_api_call("https://api.jikan.moe/v4/genres/anime")["data"]
    else:
        progressbar.increment(from_cache=True)

    genre: dict[str, str] | None = next((el for el in genre_data if el["name"] == genre_name), None)  # pyright: ignore [reportUnknownArgumentType,reportUnknownVariableType,reportGeneralTypeIssues]
    if not genre:
        print("\r", flush=True, end="")
        print(f'Genre "{genre_name}" not found.')
        sys.exit(1)

    caching.write_json("genres.json", genre_data)  # pyright: ignore [reportArgumentType]
    return genre["mal_id"]  # pyright: ignore [reportUnknownVariableType]


# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    genre, start_year = sys.argv[1], int(sys.argv[2])
    year_data = get_data_per_year(genre, start_year)

    output.print_to_terminal(year_data, genre, start_year)
    output.plot_results(year_data, genre, start_year)

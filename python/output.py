"""Docstring."""

from __future__ import annotations

import matplotlib.pyplot as plt

# ──────────────────────────────────────────────────────────────────────────────


def progressbar(char: str = "*", clean_chars: int = 0) -> None:
    """Simple progress bar."""
    if clean_chars > 0:
        print("\r" + " " * clean_chars + "\r", end="", flush=True)
        return
    print(char, end="", flush=True)


def print_to_terminal(year_data: dict[str, object], genre: str, start_year: int) -> None:
    """Remove the progress bar and print the result."""
    to_print: list[str] = [f'"{genre}" per year']

    for year, d in year_data.items():
        if int(year) < start_year:
            continue
        of_genre, total, percent = d[genre], d["total"], d[genre + "_percent"]  # pyright: ignore [reportIndexIssue,reportUnknownVariableType]
        to_print.append(f"{year}: {of_genre}/{total} ({percent}%)")

    progressbar(clean_chars=len(to_print * 2))  # remove progress bar
    print("\n".join(to_print))


def plot_results(year_data: dict[str, object], genre: str, start_year: int) -> None:
    """Plot the results via matplotlib."""
    # filter only years >= start_year
    year_data = {year: data for year, data in year_data.items() if int(year) >= start_year}

    years = list(year_data.keys())
    percentages = [data[genre + "_percent"] for data in year_data.values()]  # pyright: ignore [reportIndexIssue,reportUnknownVariableType]
    title = f"{genre} per year"

    # base plot
    fig = plt.figure(figsize=(10, 6))
    plt.plot(years, percentages, marker="o", linestyle="-", color="b", label=genre)  # pyright: ignore [reportUnknownArgumentType]

    # labels
    fig.canvas.manager.set_window_title(title)  # pyright: ignore [reportOptionalMemberAccess], https://github.com/matplotlib/matplotlib/issues/27774
    plt.title(title)
    footer = "Data: myanimelist (via Jikan API).\nSource Code: https://github.com/chrisgrieser/anime-stats"
    plt.figtext(0.1, 0.01, footer, fontsize=8)
    plt.xlabel("Year")
    plt.ylabel(f"Share of {genre} to total releases")

    plt.grid(visible=True)
    plt.legend()
    plt.show()

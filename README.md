# Anime Stats
Auto-generate some simple statistics on anime.

## Usage
```bash
# init
python3 -m venv ./.venv
source ./.venv/bin/activate 
python3 -m pip install -r requirements.txt

# run
genre="Romance" # available genres: https://api.jikan.moe/v4/genres/anime
python3 -m python.main "$genre"
```

```bash
# using `just`
just init
just genre="Romance"
```

## Example Output
```txt
ISEKAIS PER YEAR
2014: 2/187 (1%)
2015: 4/204 (2%)
2016: 7/229 (3%)
2017: 6/225 (3%)
2018: 9/224 (4%)
2019: 11/182 (6%)
2020: 8/175 (5%)
2021: 24/204 (12%)
2022: 17/189 (9%)
2023: 29/240 (12%)
2024: 24/174 (14%)
```

## Visualization
TODO

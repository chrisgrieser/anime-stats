set quiet := true

genre := "Isekai"
start_year := "2014"

#───────────────────────────────────────────────────────────────────────────────

# interactive
run-fzf:
    #!/usr/bin/env zsh
    genre=$(curl --silent "https://api.jikan.moe/v4/genres/anime" |
        yq --input-format=json '.data[] | .name' | fzf)
    [[ -z "$genre" ]] && return
    start_year="{{ start_year }}"
    source ./.venv/bin/activate
    python3 -m python.main "$genre" "$start_year"

# streaming
run:
    #!/usr/bin/env zsh
    source ./.venv/bin/activate
    year=2022 # shorter for quicker debugging
    python3 -m python.main "{{ genre }}" "$year"

flush-cache:
    rm -vrf ./cache

[macos]
open-api-docs:
    open "https://docs.api.jikan.moe/"

init:
    [[ ! -d ./.venv ]] || rm -rf ./.venv
    python3 -m venv ./.venv
    source ./.venv/bin/activate && python3 -m pip install -r requirements.txt

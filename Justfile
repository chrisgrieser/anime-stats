set quiet := true

genre := "Comedy"

#───────────────────────────────────────────────────────────────────────────────

run:
    #!/usr/bin/env zsh
    source ./.venv/bin/activate
    python3 -m python.main "{{ genre }}"

run_fzf:
    #!/usr/bin/env zsh
    genre=$(curl --silent "https://api.jikan.moe/v4/genres/anime" | 
        yq --input-format=json '.data[] | .name' | fzf)
    source ./.venv/bin/activate
    python3 -m python.main "$genre"

init:
    [[ ! -d ./.venv ]] || rm -rf ./.venv
    python3 -m venv ./.venv
    source ./.venv/bin/activate && python3 -m pip install -r requirements.txt

open_api_docs:
    open "https://docs.api.jikan.moe/"


set quiet := true

genre := "Isekai"
start_year := "2014"

#───────────────────────────────────────────────────────────────────────────────

run_fzf:
    #!/usr/bin/env zsh
    if test -t 1 ; then
        genre=$(curl --silent "https://api.jikan.moe/v4/genres/anime" |
            yq --input-format=json '.data[] | .name' | fzf)
        if test -z "$genre" ; then
            echo "No genre selected, aborting."
            return
        fi
        start_year="{{ start_year }}"
    else
        # fallback when not connected to terminal, e.g., via IDE task runner
        genre="{{ genre }}"
        start_year=2019
    fi
    source ./.venv/bin/activate
    python3 -m python.main "$genre" "$start_year"

flush_cache:
    rm -vrf ./cache

[macos]
open_api_docs:
    open "https://docs.api.jikan.moe/"

run:
    #!/usr/bin/env zsh
    python3 -m python.main "{{ genre }}" "{{ start_year }}"
    source ./.venv/bin/activate

init:
    [[ ! -d ./.venv ]] || rm -rf ./.venv
    python3 -m venv ./.venv
    source ./.venv/bin/activate && python3 -m pip install -r requirements.txt

set quiet := true

run:
	source ./.venv/bin/activate && python3 -m python.main

init:
	[[ ! -d ./.venv ]] || rm -rf ./.venv
	python3 -m venv ./.venv
	source ./.venv/bin/activate && python3 -m pip install -r requirements.txt

open_api_docs:
    #!/usr/bin/env zsh
    if [[ "$OSTYPE" =~ "darwin" ]]; then
        open "https://docs.api.jikan.moe/"
    else
        echo "Not on MacOS."
    fi

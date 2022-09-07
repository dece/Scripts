#!/bin/bash

ensure_has() {
    if ! command -v "$1" > /dev/null; then
        echo "Can't find $1."
        exit 1
    fi
}

ensure_has fdfind
ensure_has fzf
ensure_has install-script

fdfind -t x \
    | fzf -m --layout=reverse \
    | while read -r script; do install-script "$script"; done

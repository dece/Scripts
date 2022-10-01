#!/bin/bash
# Install scripts from this repo using our neighbour paf.sh.
# Requires fdfind and fzf to work.

script_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd )"
paf="$script_dir/paf.sh"

fdfind -t x | fzf --multi --layout=reverse --header="Pick scripts to install" \
    | while read -r script; do "$paf" "$script"; done

#!/bin/bash
# Install scripts from this repo using our neighbour paf.sh.
# Requires fdfind and fzf to work.

our_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd )"
paf="$our_dir/paf.sh"
scripts_dir="$1"
[[ -z "$scripts_dir" ]] && scripts_dir="$our_dir"

fdfind -t x . "$scripts_dir" \
    | fzf --multi --layout=reverse --header="Pick scripts to install" \
    | while read -r script; do "$paf" "$script"; done

#!/bin/bash
# Create a Gemtext index from the files in the directory and their main title.
# Spaces in file names are escaped (but not tabs or other heresies).

usage() {
    echo "Usage: $0 [-h] [DIR]"
    echo "Print a Gemtext index of the directory."
    echo "  -h     show usage"
    echo "  DIR    use this directory instead of the working dir"
}

[[ "$1" == "-h" ]] && usage && exit 0

DIR="${1:-.}"
for file in "$DIR"/*.gmi; do
    title="$(head -n 1 "$file" | cut -c 3-)"
    echo "=> ${file// /%20} $title"
done

#!/bin/bash
# Quick grep for emojis from the terminal.
# You first have to download the UCD archive. It's only a few MB compressed.
# I use ripgrep for its speed but you can replace GREP by what you see fit.
# Bonus! Use this bash function to copy the first result in your X clipboard:
# mj() { emoji -u "$1" | xclip ; echo "$(xclip -o)" }
# Made with 💖 by dece. s/o to mon loulou, the bash samurai. License: WTFPLv2.

UCD_URL="https://www.unicode.org/Public/UCD/latest/ucdxml/ucd.all.flat.zip"
DIR="$HOME/.local/share/emoji"
LIST="$DIR/emojis.txt.gz"
GREP="rg"

usage() {
    echo "Usage: $0 [OPTION]... FILTER"
    echo "Display emojis based on the name filter provided."
    echo "  -h        show usage"
    echo "  -n        hide emoji name"
    echo "  -l LIMIT  limit number of output lines"
    echo "  -u        unique result (equals -n and -l 1), no new line"
    echo "  -c        show code point"
    echo "  -d        download UCD zip to create list file (requires curl)"
}

[ $# -eq 0 ] && usage && exit

download_ucdxml() {
    [ ! -d "$DIR" ] && mkdir -p "$DIR"
    unc_list="${LIST%.gz}"
    curl -L "$UCD_URL" | zcat | "$GREP" 'Emoji="Y"' | while read -r line; do
        codepoint="$(echo "$line" | sed -E 's/.* cp="([0-9A-F]+)".*/\1/g')"
        name="$(echo "$line" | sed -E 's/.* na="([^"]+)".*/\1/g')"
        echo "$codepoint;$name" >> "$unc_list"
    done
    gzip "$unc_list"
}

HIDE_NAME=
LIMIT=
NO_NEW_LINE=
SHOW_CP=
while getopts "hdnl:uc" OPTION; do
    case $OPTION in
        h) usage; exit 0 ;;
        d) download_ucdxml; exit $? ;;
        n) HIDE_NAME=true ;;
        l) LIMIT=$OPTARG ;;
        u) HIDE_NAME=true; LIMIT=1; NO_NEW_LINE=true ;;
        c) SHOW_CP=true ;;
        *) usage; exit 1 ;;
    esac
done
shift $(( OPTIND - 1 ))
FILTER="$*"

if [ ! -f "$LIST" ]; then
    echo "Can't find list file at $LIST. Use -d to download it!"
    exit 1
fi

line_id=0
zcat "$LIST" | "$GREP" -i "$FILTER" | while read -r line; do
    [ -n "$LIMIT" ] && (( line_id >= LIMIT )) && break
    readarray -d ";" -t elements <<< "$line"
    codepoint="${elements[0]}"
    result="$(echo -e "\\U$codepoint")"
    if [ "$HIDE_NAME" != true ]; then
        name="${elements[1]}"
        result="$result $(echo "$name" | tr '[:upper:]' '[:lower:]')"
    fi
    if [ "$SHOW_CP" = true ]; then
        result="$result (U+$codepoint)"
    fi
    [ "$NO_NEW_LINE" = true ] && echo_opt="-n" || echo_opt=""
    echo "$echo_opt" "$result"
    line_id=$(( line_id + 1 ))
done

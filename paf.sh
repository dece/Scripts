#!/bin/bash -e
# A script to install other scripts! Create a symbolic link to the path passed
# as first argument in ~/.local/bin and strip the extension. If a second
# argument is passed, this name is used (unstripped) instead. If a file already
# exists at the link path, the script fails (last command is ln itself). This is
# intentional.

usage() {
    echo "Usage: $0 script [link_name]"
    echo "  script     script or executable to install"
    echo "  link_name  name to use for the symbolic link"
}

[ $# -lt 1 ] || [ $# -gt 2 ] && usage && exit 1

script_dir="$HOME/.local/bin"
script="$(realpath "$1")"
[ ! -f "$script" ] && echo "$script does not exist." && exit 1
[ ! -x "$script" ] && echo "$script is not executable." && exit 1

if [[ -n "$2" ]]; then
    script_name="$2"
else
    script_name="$(basename "$script")"
    script_name="${script_name%.*}"  # remove extension
fi

ln -s "$script" "$script_dir/$script_name"

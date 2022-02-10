#!/bin/zsh -e
# Short Zsh script to compare some of my manually installed software against
# what is apparently available on Github, PyPI or whatever remote hell.
# Requires curl.

GH="https://github.com"
GH_TAIL="releases/latest"

get_latest_tag() {
    redirect="$(curl "$1" -v 2>&1 | grep "^< location:")"
    echo "${redirect##*/}"
}

check_neovim() {
    echo "# Neovim"
    echo "Installed: $(nvim -v | head -n 1)"
    echo "Available: $(get_latest_tag "$GH/neovim/neovim/$GH_TAIL")"
}

check_alacritty() {
    echo "# Alacritty"
    echo "Installed: $(alacritty -V)"
    echo "Available: $(get_latest_tag "$GH/alacritty/alacritty/$GH_TAIL")"
}

check_cheat() {
    echo "# Cheat"
    echo "Installed: $(cheat -v)"
    echo "Available: $(get_latest_tag "$GH/cheat/cheat/$GH_TAIL")"
}

check_python_packages() {
    echo "# Python user packages"
    pip3 list -o --user
}

(( $+commands[nvim] )) && check_neovim
(( $+commands[alacritty] )) && check_alacritty
(( $+commands[cheat] )) && check_cheat
check_python_packages

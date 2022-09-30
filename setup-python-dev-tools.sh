#!/bin/bash

ask_install() {
    packages="$@"
    read -p "Install $packages? [y/n] " -n 1 -r ; echo
    [[ "$REPLY" = y ]] && pip3 install $packages
}

ask_install jedi-language-server
ask_install pycodestyle
ask_install pylint
ask_install mypy

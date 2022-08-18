#!/bin/bash

pip3 install python-lsp-server

ask_install() {
    packages="$@"
    read -p "Install $packages? [y/n] " -n 1 -r ; echo
    [[ "$REPLY" = y ]] && pip3 install $packages
}

ask_install pyflakes
ask_install black python-lsp-black
ask_install mypy pylsp-mypy

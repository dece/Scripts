#!/bin/bash
# Purge a systemd service that won't gtfo.

usage() {
    echo "Usage: $0 [service name, without .service]"
}

[ $# -ne 1 ] && usage && exit
name="$1"

sudo systemctl stop "$name"
sudo systemctl disable "$name"
fdfind "$name" /etc/systemd/system -t f -t l -x sudo rm -i
fdfind "$name" /usr/lib/systemd/system -t f -t l -x sudo rm -i
sudo systemctl daemon-reload
sudo systemctl reset-failed

#!/bin/bash
# Mount the first phone to be found in a temporary directory with a name
# prefixed with "jmtpfs", in the /tmp directory. If -u is passed, unmount all
# directories with this same name pattern and remove them (after confirmation).

if ! command -v jmtpfs > /dev/null; then
    echo "jmtpfs is not installed."
    exit
fi

if [[ "$1" = "-u" ]]; then
    for mount_dir in /tmp/jmtpfs.*; do
        if [ -d "$mount_dir" ]; then
            umount "$mount_dir"
            echo "$mount_dir unmounted. It should now be empty:"
            ls -la "$mount_dir"
            rm -rI "$mount_dir"
        fi
    done
    exit
fi

mount_dir="$(mktemp -d -p /tmp jmtpfs.XXXXXXXXXX)"
jmtpfs "$mount_dir"
echo "Mount directory: $mount_dir"

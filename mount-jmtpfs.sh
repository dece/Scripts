#!/bin/bash
# Mount the first phone to be found in a temporary directory with a name
# prefixed with "jmtpfs", in the /tmp directory. If -u is passed, unmount all
# directories with this same name pattern and remove them (after confirmation).

if ! command -v jmtpfs > /dev/null; then
    echo "jmtpfs is not installed."
    exit
fi

unmount_phones() {
    for mount_dir in /tmp/jmtpfs.*; do
        if [ -d "$mount_dir" ]; then
            umount "$mount_dir"
            echo "$mount_dir unmounted. It should now be empty:"
            ls -la "$mount_dir"
            rm -rI "$mount_dir"
        fi
    done
}

SHOW_MOUNT=
while getopts "hus" OPTION; do
    case $OPTION in
        h) usage; exit 0 ;;
        u) unmount_phones; exit 0 ;;
        s) SHOW_MOUNT=true ;;
        *) usage; exit 1 ;;
    esac
done

mount_dir="$(mktemp -d -p /tmp jmtpfs.XXXXXXXXXX)"
jmtpfs "$mount_dir"
echo "Mount directory: $mount_dir"
[[ "$SHOW_MOUNT" = true ]] && nohup open "$mount_dir" > /dev/null 2>&1

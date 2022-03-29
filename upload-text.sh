#!/bin/bash -e
# Upload a text file to a server through SSH so that it can be shared.
# This script expects the server can serve files on the Web. Also expects curl.
# It uses an HTML template instead of the raw text file because browsers
# sometimes do not expect UTF-8 by default and this is always what I upload.
#
# You need to provide those 3 env variables:
# - REMOTE_DEST: the SSH destination to reach
# - REMOTE_WWW: the remote path where the HTML file will be stored
# - REMOTE_URL: the URL of the directory to print; file name is appended

usage() {
    echo "Usage: $0 text_file"
    echo "Upload a text file to a simple HTML template on a server."
}

[ $# -ne 1 ] && usage && exit

# If a file exists at that path, it is sourced; you can put your env vars here.
CONFIG_PATH="$HOME/.config/upload-text.conf"
[ -f "$CONFIG_PATH" ] && . "$CONFIG_PATH"

# Generate a simple HTML page from the content.
BASENAME="$(basename "$1")"
HTML_FILE="$(mktemp)"
cat << EOF > "$HTML_FILE"
<!doctype html>
<html>
<head>
    <meta charset="UTF-8">
    <title>$BASENAME</title>
    <style>
        body { max-width: 40em; }
    </style>
</head>
<body>
$(cat "$1")
</body>
</html>
EOF

# Upload the HTML file through SSH. Using SSH rather than SCP allows us to write
# the file in one connection while setting appropriate rights.
REMOTE_FILE="$(mktemp -u -p "$REMOTE_WWW" XXXXXXXXXX.html)"
cat "$HTML_FILE" | ssh -q "$REMOTE_DEST" "umask 027; cat > '$REMOTE_FILE'"
rm "$HTML_FILE"

# Show the remote file path.
echo "$REMOTE_URL/$(basename "$REMOTE_FILE")"

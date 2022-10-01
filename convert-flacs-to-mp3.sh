#!/bin/bash -ex
# Convert FLACs in a directory to MP3 files (V0, but configure it below).
# Requires fdfind and ffmpeg.
fdfind -t f -e flac . "$1" | while read -r flac; do
    mp3="${flac/%flac/mp3}"
    ffmpeg -i "$flac" -codec:a libmp3lame -q:a 0 "$mp3" && rm "$flac"
done

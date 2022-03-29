#!/bin/bash
# Brutally reset file permissions to sane defaults for files/folders that have
# been tainted by a poorly mounted NTFS drive (777).
pushd "$1"
fdfind -t f -x chmod 644
fdfind -t d -x chmod 755
popd

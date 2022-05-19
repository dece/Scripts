#!/bin/bash
# Open Python PDF docs.

if [ ! -v PYTHON_DOCS_PATH ]; then
    echo "You need to define PYTHON_DOCS_PATH."
    exit
fi

if [[ -n "$1" ]]; then
    filename="$(find "$PYTHON_DOCS_PATH" -type f -name "*$1*" | head -n 1)"
else
    filename="$PYTHON_DOCS_PATH/library.pdf"
fi

nohup open "$filename" > /dev/null 2>&1

#!/bin/bash -e
# Check available updates for manually installed Python packages.
table="$(pip list --user --outdated)"
echo "$table"
list="$(echo "$table" | tail -n +3 | awk '{print $1}' | tr '\n' ' ')"
echo "Update the all with: $ pip install -U $list"

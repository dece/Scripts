#!/bin/bash
# Delete a branch both locally and on origin.
BRANCH_NAME="$1"
git branch -D $BRANCH_NAME
git push --delete origin $BRANCH_NAME

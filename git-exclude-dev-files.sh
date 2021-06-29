#!/bin/bash
# Ignore user-specific dev files without cluttering the gitignore files.
# Other team members may not care that you use Vim, VS Code, an IDEA product or
# whatever, so it is a bit weird to commit your own specific tooling ignore
# patterns into the project. Use your local exclude file instead.

exclude() {
    if ! grep "$1" .git/info/exclude > /dev/null ; then
        echo "$1" >> .git/info/exclude
    fi
}

exclude '.*.swp'
exclude '.vscode/'

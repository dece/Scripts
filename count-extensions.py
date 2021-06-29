#!/usr/bin/env python3
# Dumb script to print statistics of file extensions in the current directory.

import os
import os.path
from collections import defaultdict

def count_extensions(folder):
    stats = defaultdict(int)
    for (root, dirs, files) in os.walk(folder):
        for f in files:
            ext = os.path.splitext(f)[1].lstrip(".")
            stats[ext] += 1
    return stats

if __name__ == "__main__":
    stats = count_extensions(".")
    stats_list = reversed(sorted([(n, e) for e, n in stats.items()]))
    for n, e in stats_list:
        print("{}\t{}".format(n, e))

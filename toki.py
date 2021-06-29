#!/usr/bin/env python3
# type: ignore
"""Cheat sheet for Toki Pona, using the nimi ale pona table. License WTFPLv2.

You need a CSV export of the nimi ale pona (inli). Place it in the path stored
in the CSV variable below, or change that variable to suit your needs. It can be
downloaded from the following link:
https://docs.google.com/spreadsheets/d/1t-pjAgZDyKPXcCRnEdATFQOxGbQFMjZm-8EvXiQd2Po/edit#gid=0

If colorama is installed on your system (it often is for some reason), the
output will be colored; else it will still properly display text.
"""

import argparse
import csv
from pathlib import Path

CSV = Path.home() / ".local/share/toki/nimi-ale-pona.csv"

try:
    from colorama import Fore, init, Style
except ImportError:
    class Dummy:
        def __getattr__(self, _):
            return ""
    Fore = Dummy()
    Style = Dummy()
else:
    init()

def main():
    argparser = argparse.ArgumentParser(description="nimi ale pona!")
    argparser.add_argument("word", nargs="?", help="word to search")
    args = argparser.parse_args()

    with open(CSV) as nap_file:
        nap_csv = csv.DictReader(nap_file)
        if args.word:
            for row in nap_csv:
                words = row["word"].split(", ")
                if args.word in words:
                    print_row(row)
                    break
            else:
                print("nimi ala!")
        else:
            for row in nap_csv:
                print_row(row)

COLORED_CATS = {  # soweli suwi kule!
    "pu": f"{Fore.GREEN}pu{Fore.RESET}",
    "pre-pu": f"{Fore.CYAN}pre-pu{Fore.RESET}",
    "post-pu": f"{Fore.MAGENTA}post-pu{Fore.RESET}",
}

def print_row(row):
    word_line = f"{Style.BRIGHT}{row['word']}{Style.NORMAL}"
    category = COLORED_CATS.get(row["category"], "?")
    definition = row['definition'].strip().replace("\n", "")
    word_line += f" ({category}): {definition}"
    print(word_line)
    details = f"from {row['source language']}"
    etymology = row['etymology'].strip().replace("\n", "") 
    if etymology:
        details += ": " + etymology
    print(f"  {Style.DIM}{details}{Style.RESET_ALL}")
    if row['tags']:
        print(f"  {Style.DIM}{row['tags']}{Style.RESET_ALL}")
    if row['']:  # bogus second tag columns
        print(f"  {Style.DIM}{row['']}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

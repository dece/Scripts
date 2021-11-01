#!/usr/bin/env python3
"""Translate words from the terminal using WordReference. Licence WTFPLv2.

As the website frontend is rather stable now it should not break completely but
weird thing could show up on some cases I missed; tell me if you find a bug!

Requires requests and beautifulsoup4 on your system; the Debian packages for
both are fine.

If colorama is installed on your system (it often is for some reason), the
output will be colored; else it will still properly display text.
"""

import argparse
import dataclasses
import enum
import urllib.parse
from shutil import which

import requests
from bs4 import BeautifulSoup, NavigableString


class DummyColorama:
    def __getattr__(self, _):
        return ""


HAS_COLORAMA = True
Fore = None
Style = None

try:
    import colorama
except ImportError:
    HAS_COLORAMA = False
    Fore = DummyColorama()
    Style = DummyColorama()

URL = "https://www.wordreference.com"

MeaningType = enum.Enum("MeaningType", "MAIN ADD COMPOUND")


@dataclasses.dataclass
class Translation:
    desc: str
    nature: str
    precision: str = ""


@dataclasses.dataclass
class Meaning:
    ident: str
    mtype: MeaningType
    original: str = ""
    nature: str = ""
    desc: list[str] = dataclasses.field(default_factory=list)
    ex: list[str] = dataclasses.field(default_factory=list)
    trans: list[Translation] = dataclasses.field(default_factory=list)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lang", help="4-letter code, e.g. 'fren' or 'enfr'")
    ap.add_argument("words", nargs="+", help="word or words to translate")
    ap.add_argument("-s", "--suggestions", action="store_true",
                    help="show suggestions instead of translations")
    ap.add_argument("-C", "--no-color", action="store_true",
                    help="disable colors")
    args = ap.parse_args()

    global Fore, Style
    if args.no_color and HAS_COLORAMA:
        Fore = DummyColorama()
        Style = DummyColorama()
    else:
        Fore = colorama.Fore
        Style = colorama.Style
        colorama.init()

    lang = args.lang
    words = " ".join(args.words)

    if args.suggestions:
        get_suggestions(lang, words)
    else:
        get_translations(lang, words)


def get_translations(lang, words):
    """Get translations for these words."""
    encoded_words = urllib.parse.quote(words)
    response = requests.get(f"{URL}/{lang}/{encoded_words}")
    if response.status_code != 200:
        exit("Could not connect to WordReference.")

    soup = BeautifulSoup(response.text, "html.parser")
    article = soup.find(id="articleWRD")

    meanings = []
    for table in article.find_all("table"):
        # Discard error tables.
        if "WRD" not in table.get("class"):
            continue

        top_row = table.find("tr", class_="wrtopsection")
        ph_span = top_row.find("span", class_="ph")
        if ph_span:
            # Main meanings
            if ph_span.get("data-ph") == "sMainMeanings":
                parse_rows(table, meanings, MeaningType.MAIN)

            # Additional translations
            if ph_span.get("data-ph") == "sAddTrans":
                parse_rows(table, meanings, MeaningType.ADD)

        # Compound forms
        if table.get("id") == "compound_forms":
            parse_rows(table, meanings, MeaningType.COMPOUND)

    for meaning in meanings:
        print_meaning(meaning)


def parse_rows(table, meanings, mtype):
    """Parse all good rows of this table and store results in meanings."""
    meaning = None
    for row in table.find_all("tr"):
        # Discard rows that aren't meanings.
        row_classes = row.get("class")
        if all(c not in row_classes for c in ("even", "odd")):
            continue

        # New meaning start with a row that has an ID.
        is_new_meaning_row = False
        if (meaning_id := row.get("id")):
            if meaning:
                meanings.append(meaning)
            meaning = Meaning(ident=meaning_id, mtype=mtype)
            is_new_meaning_row = True

        cells = row.find_all("td")

        # Rows with 3 cells are definitions or complementary meanings.
        if len(cells) == 3:
            parse_common_cells(cells, meaning, is_new_meaning_row)
        # Rows with 2 cells are examples.
        else:
            parse_example_cells(cells, meaning)

    if meaning:
        meanings.append(meaning)


def parse_common_cells(cells, meaning, is_new_meaning):
    """Parse common cells: meaning, definition, translations, etc."""
    lcell, ccell, rcell = cells

    # For new meanings, use the left cell info.
    if is_new_meaning:
        meaning.original = lcell.strong.text
        if (nature_elements := lcell.em.contents):
            meaning.nature = nature_elements[0]

    # Each 3-cell row is a translation.
    trans_desc = []
    for content in rcell.contents:
        if isinstance(content, NavigableString):
            trans_desc.append(content.strip())
        elif "POS2" not in (content.get("class") or []):
            trans_desc.append(content.text)
    nature = ""
    if (nature_content := rcell.contents[-1]):
        if len(nature_content):
            nature = nature_content.contents[0]
    translation = Translation(desc=" ".join(trans_desc), nature=nature)

    # Center cell mixes original description and translation info…
    for child in ccell.children:
        # "dsense" classes are for this specific translation,
        # not the current "row-group" meaning.
        if not isinstance(child, NavigableString):
            if "dsense" in (child.get("class") or []):
                translation.precision += child.text
            elif (text := child.text.strip()):
                meaning.desc.append(text)
        elif (text := str(child).strip()):
            meaning.desc.append(text)
    meaning.trans.append(translation)


def parse_example_cells(cells, meaning):
    """Parse cells of an example line (pretty much just the last one)."""
    meaning.ex.append(cells[-1].span.text)


def print_meaning(meaning):
    """Print a few formatted lines for this meaning."""
    meaning_colors = {
        MeaningType.MAIN: Fore.GREEN,
        MeaningType.ADD: Fore.CYAN,
        MeaningType.COMPOUND: Fore.MAGENTA,
    }

    # First line contains the original word and its definition.
    first_line = (
        meaning_colors[meaning.mtype] +
        f"{Style.BRIGHT}{meaning.original}{Style.NORMAL}{Fore.RESET} "
    )
    if meaning.nature:
        first_line += f"{Style.DIM}({meaning.nature}){Style.NORMAL} "
    first_line += " ".join(meaning.desc)
    print(first_line)
    # Each translation is on its own line.
    for trans in meaning.trans:
        trans_line = f"— {trans.desc}"
        if trans.nature:
            trans_line += f" {Style.DIM}({trans.nature}){Style.NORMAL}"
        if trans.precision:
            trans_line += f" {Style.DIM}{trans.precision}{Style.NORMAL}"
        print(trans_line)
    # Show examples on different, dimmed line.
    for example in meaning.ex:
        print(f"  {Style.DIM}e.g. {example}{Style.NORMAL}")


AUTOCOMP_URL = f"{URL}/2012/autocomplete/autocomplete.aspx"


def get_suggestions(lang, words):
    """Show completion suggestions for these words."""
    params = {"dict": lang, "query": words}
    response = requests.get(AUTOCOMP_URL, params=params)
    if response.status_code != 200:
        exit("Could not connect to WordReference.")

    # The response is rows of tab-separated values. 1st record is the word
    # itself, 2nd is its language. The 3rd is an integer that I guess matches
    # the word popularity or a similarity score to the query… anyway it can be
    # used for sorting. 4th record is 0 or 1 if the word has conjugation
    # available.
    suggestions = (
        line.rstrip().split("\t")
        for line in response.text.splitlines()
    )

    # If FZF is available, let the user pick a word to perform the search.
    if (fzf := which("fzf")):
        from subprocess import CalledProcessError, PIPE, Popen
        process = Popen([fzf], stdin=PIPE, stdout=PIPE)
        input_data = "\n".join(
            f"{word} [{wlang}, {pop}, {conj}]"
            for word, wlang, pop, conj in suggestions
        ).encode()
        try:
            stdout, _ = process.communicate(input_data)
        except CalledProcessError:
            exit("Could not call FZF.")
        result = stdout.decode().split("[", maxsplit=1)[0]
        get_translations(lang, result)
    # Else just display the suggestions with information.
    else:
        for word, wlang, pop, conj in suggestions:
            output = f"[{wlang}] {word} ({pop})"
            if conj == "1":
                output += " (conj.)"
            print(output)


if __name__ == "__main__":
    main()

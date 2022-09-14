#!/usr/bin/env python3
"""Download tracklists from djtracklists.com."""

import argparse

import requests
from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--series", help="download this series")
    parser.add_argument("-t", "--tracklist", help="download this tracklist")
    args = parser.parse_args()

    if tracklist_url := args.tracklist:
        download_tracklist(tracklist_url)


def is_track_row(css_class: str) -> bool:
    return css_class == "on" or css_class == "off"


def download_tracklist(url: str):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for row in soup.find_all("div", class_=is_track_row):
        print("*" * 80)
        try:
            print("track", row.find("a", class_="track").string)
            print("release", row.find("a", class_="release").string)
        except AttributeError:
            print("track", row.find("b").string)
        for artist in row.find_all("a", class_="artist"):
            prev_tag = artist.previous_sibling.string
            if getattr(prev_tag, "string", "").strip() == "remixed  by":
                print("remixing artist", artist.string)
            else:
                print("artist", artist.string)
        print("\n" * 10)


if __name__ == "__main__":
    main()

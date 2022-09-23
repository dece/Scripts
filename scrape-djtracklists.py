#!/usr/bin/env python3
"""Download tracklists from djtracklists.com."""

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup


@dataclass
class Track:
    title: str
    artists: list[str]
    mix: Optional[str]
    mix_artists: Optional[list[str]]
    timestamp: str


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--series", help="download this series")
    parser.add_argument("-t", "--tracklist", help="download this tracklist")
    args = parser.parse_args()

    if tracklist_url := args.tracklist:
        tracklist = download_tracklist(tracklist_url)
        name = tracklist_url.rstrip("/").rsplit("/", maxsplit=1)[-1]
        file_name = Path.cwd() / (name + ".txt")
        save_tracklist(tracklist, file_name)


def is_track_row(css_class: str) -> bool:
    return css_class in ("on", "off")


def download_tracklist(url: str) -> list[Track]:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    tracklist = []
    for row in soup.find_all("div", class_=is_track_row):
        artists = []
        mix_artists = []
        try:
            title = row.find("a", class_="track").string
            mix = row.find("a", class_="release").string
        except AttributeError:
            title = row.find("b").string
            mix = None
        timestamp = row.find("span", class_="index_time").string
        for artist in row.find_all("a", class_="artist"):
            prev_tag = artist.previous_sibling.string
            if getattr(prev_tag, "string", "").strip() == "remixed  by":
                mix_artists.append(artist.string)
            else:
                artists.append(artist.string)
        tracklist.append(
            Track(
                title=title,
                mix=mix,
                artists=artists,
                mix_artists=mix_artists or None,
                timestamp=timestamp,
            )
        )
    return tracklist


def save_tracklist(tracklist: list[Track], file_name: Path):
    try:
        with open(file_name, "wt", encoding="utf8") as file:
            for track in tracklist:
                artists = " & ".join(track.artists)
                line = f"{track.timestamp} — {artists} — {track.title}"
                if track.mix:
                    line += f" ({track.mix})"
                if track.mix_artists:
                    mix_artists = " & ".join(track.mix_artists)
                    line += f" remixed by {mix_artists}"
                file.write(line + "\n")
    except OSError as exc:
        print(f"Can't save tracklist: {exc}")


if __name__ == "__main__":
    main()

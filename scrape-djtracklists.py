#!/usr/bin/env python3
"""Download tracklists from djtracklists.com as CSV."""

import argparse
import csv
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup


@dataclass
class Track:
    """One track, parsed from a tracklist page."""
    title: str
    artists: list[str]
    mix: Optional[str]
    mix_artists: Optional[list[str]]
    timestamp: str

    def format_artists(self):
        return " & ".join(self.artists)

    def format_mix_artists(self):
        return " & ".join(self.mix_artists) if self.mix_artists else ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--series",
                        help="download this series (provide URL of 1st page)")
    parser.add_argument("-t", "--tracklist",
                        help="download this tracklist (provide URL)")
    parser.add_argument("--pretty", help="pretty print a CSV file.")
    args = parser.parse_args()

    if csv_file_name := args.pretty:
        pretty_print_csv(csv_file_name)
    elif series_url := args.series:
        download_series(series_url)
    elif tracklist_url := args.tracklist:
        download_tracklist(tracklist_url)


def download_series(series_url: str):
    while series_url:
        print("Processing series URL", series_url)
        response = requests.get(series_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # Download all tracklists.
        for tracklist_link in soup.find_all("a", class_="mix"):
            tracklist_url = tracklist_link["href"]
            print("Processing tracklist URL", tracklist_url)
            download_tracklist(tracklist_url)
            time.sleep(1)  # throttle
        # Look for the next page button.
        for page_link in soup.find_all("a", class_="pagenumber"):
            if "Next" in page_link.string:
                series_url = page_link["href"]
                break
        else:
            series_url = None


def download_tracklist(url: str):
    tracklist = get_tracklist_from_url(url)
    name = url.rstrip("/").rsplit("/", maxsplit=1)[-1]
    file_name = Path.cwd() / (name + ".csv")
    save_tracklist_as_csv(tracklist, file_name)


def is_track_row(css_class: str) -> bool:
    return css_class in ("on", "off")


def get_tracklist_from_url(url: str) -> list[Track]:
    """Get tracklist from the Web and parse it into a list of Track objects."""
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
            try:
                title = row.find("b").string
            except AttributeError:
                title = "(unknown title)"
            mix = None

        try:
            timestamp = row.find("span", class_="index_time").string
        except AttributeError:
            timestamp = "(unknown timestamp)"

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


def save_tracklist_as_csv(tracklist: list[Track], file_name: Path):
    try:
        with open(file_name, "wt", encoding="utf8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Timestamp", "Artists", "Title", "Mix", "Remix artists"]
            )
            for track in tracklist:
                writer.writerow([
                    track.timestamp,
                    track.format_artists(),
                    track.title,
                    track.mix or "",
                    track.format_mix_artists(),
                ])
    except OSError as exc:
        print(f"Can't save tracklist: {exc}")


def pretty_print_csv(csv_file_name: str):
    try:
        with open(csv_file_name, "rt", encoding="utf8", newline="") as file:
            reader = csv.reader(file)
            first_line_skipped = False
            for row in reader:
                if not first_line_skipped:
                    first_line_skipped = True
                    continue
                ts, artists, title, mix, remix_artists = row
                if ":" in ts:
                    ts_min, ts_sec = ts.split(":")
                    ts_min = int(ts_min)
                    ts_h, ts_min = ts_min // 60, ts_min % 60
                    ts = f"{ts_h:02}:{ts_min:02}:{ts_sec}"
                print(f"{ts}  {artists or '(unknown)'} — {title}", end="")
                if mix:
                    print(f"  ({mix})", end="")
                    if remix_artists:
                        print(f" by {remix_artists}", end="")
                print()
    except OSError as exc:
        print(f"Can't read CSV: {exc}")


if __name__ == "__main__":
    main()

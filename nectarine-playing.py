#!/usr/bin/env python3
"""Python bindings to the Nectarine Queue interface

If used as a script, print on stdout the current track song and artist(s).

It's mainly useful if you work with terminals around and don't want to keep the
Nectarine tab under your eyes all the time (even if it's raina's design).
Respect their servers, and long live Nectarine!

Requirements: the requests package.
"""

import sys
import xml.etree.ElementTree as ElementTree
from dataclasses import dataclass

import requests

QUEUE_URL = "https://scenestream.net/demovibes/xml/queue/"


@dataclass
class Artist:
    ident: int
    flag: str
    name: str


@dataclass
class Song:
    ident: int
    length: str
    title: str


@dataclass
class Requester:
    flag: str
    name: str


@dataclass
class Entry:
    request_time: str
    artists: list[Artist]
    song: Song
    requester: Requester
    playstart: str


def get_queue_xml(url=QUEUE_URL):
    """Return the XML tree from the API, or None on error."""
    response = requests.get(url)
    if response.status_code != 200:
        sys.stderr.write(f"Failed to open URL: {QUEUE_URL}")
        return None
    return ElementTree.XML(response.text)


def get_now_playing(queue_xml):
    """Return the Entry of the currently playing song."""
    entry_node = queue_xml.find("now").find("entry")
    return parse_entry(entry_node)


def parse_entry(entry_node) -> Entry:
    artists = entry_node.findall("artist")
    song = entry_node.find("song")
    req = entry_node.find("requester")
    playstart = entry_node.find("playstart")
    return Entry(
        request_time=entry_node.get("request_time"),
        artists=[
            Artist(
                ident=artist.get("id"),
                flag=artist.get("flag"),
                name=artist.text,
            )
            for artist in artists
        ],
        song=Song(
            ident=song.get("id"),
            length=song.get("length"),
            title=song.text,
        ),
        requester=Requester(
            flag=req.get("flag"),
            name=req.text,
        ),
        playstart=playstart.text,
    )


def main():
    queue_xml = get_queue_xml()
    if queue_xml is None:
        return
    now_playing = get_now_playing(queue_xml)

    print(
        "{artists} — {song} [{length}] — requested by {req}".format(
            artists=(
                " & ".join(
                    f"{a.name} ({a.flag})"
                    for a in now_playing.artists
                )
            ),
            song=now_playing.song.title,
            length=now_playing.song.length,
            req=now_playing.requester.name,
        )
    )


if __name__ == "__main__":
    main()

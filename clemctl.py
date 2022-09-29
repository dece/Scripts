#!/usr/bin/env python3
"""Control Clementine from the command line using dbus."""

import dbus

CLEM_NAME = "org.mpris.MediaPlayer2.clementine"
CLEM_PATH = "/org/mpris/MediaPlayer2"
CLEM_PLAYER_NAME = "org.mpris.MediaPlayer2.Player"
PROPS_NAME = "org.mpris.MediaPlayer2.Player"


def main():
    bus = dbus.SessionBus()
    hour, minutes, seconds = get_position(bus)
    timestamp = f"{minutes:02}:{seconds:02}"
    if hour:
        timestamp = f"{hour}:{timestamp}"
    print(timestamp)


def get_clementine_object(bus):
    clem_object = bus.get_object(CLEM_NAME, CLEM_PATH)
    return clem_object


def get_position(bus):
    clem_object = get_clementine_object(bus)
    position = clem_object.Get(CLEM_PLAYER_NAME, "Position")
    timestamp_ns = int(position)
    timestamp_sec = timestamp_ns // 1_000_000
    timestamp_h = timestamp_sec // 3600
    timestamp_min = (timestamp_sec // 60) % 60
    timestamp_sec = timestamp_sec % 60
    return (timestamp_h, timestamp_min, timestamp_sec)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Control Clementine from the command line using dbus."""

import argparse

import dbus  # type: ignore

CLEM_NAME = "org.mpris.MediaPlayer2.clementine"
CLEM_PATH = "/org/mpris/MediaPlayer2"
CLEM_PLAYER_NAME = "org.mpris.MediaPlayer2.Player"

# org.mpris.MediaPlayer2.Player.CanControl
# org.mpris.MediaPlayer2.Player.CanGoNext
# org.mpris.MediaPlayer2.Player.CanGoPrevious
# org.mpris.MediaPlayer2.Player.CanPause
# org.mpris.MediaPlayer2.Player.CanPlay
# org.mpris.MediaPlayer2.Player.CanSeek
# org.mpris.MediaPlayer2.Player.LoopStatus
# org.mpris.MediaPlayer2.Player.MaximumRate
# org.mpris.MediaPlayer2.Player.Metadata
# org.mpris.MediaPlayer2.Player.MinimumRate
# org.mpris.MediaPlayer2.Player.Next
# org.mpris.MediaPlayer2.Player.OpenUri
# org.mpris.MediaPlayer2.Player.Pause
# org.mpris.MediaPlayer2.Player.Play
# org.mpris.MediaPlayer2.Player.PlayPause
# org.mpris.MediaPlayer2.Player.PlaybackStatus
# org.mpris.MediaPlayer2.Player.Position
# org.mpris.MediaPlayer2.Player.Previous
# org.mpris.MediaPlayer2.Player.Rate
# org.mpris.MediaPlayer2.Player.Seek
# org.mpris.MediaPlayer2.Player.SetPosition
# org.mpris.MediaPlayer2.Player.Shuffle
# org.mpris.MediaPlayer2.Player.Stop
# org.mpris.MediaPlayer2.Player.Volume


def main():
    parser = argparse.ArgumentParser()

    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument("--play", action="store_true")
    action_group.add_argument("--play-pause", action="store_true")
    action_group.add_argument("--pause", action="store_true")
    action_group.add_argument("--stop", action="store_true")
    action_group.add_argument("--previous", action="store_true")
    action_group.add_argument("--next", action="store_true")

    subparsers = parser.add_subparsers()

    pos_parser = subparsers.add_parser("position", help="get track position")
    pos_parser.add_argument("-f", "--format", help="position format")
    pos_parser.set_defaults(func=handle_position_command)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
        return

    bus = dbus.SessionBus()
    clem_object = get_clementine_object(bus)
    if args.play:
        get_player_interface(clem_object).Play()
    elif args.play_pause:
        get_player_interface(clem_object).PlayPause()
    elif args.pause:
        get_player_interface(clem_object).Pause()
    elif args.stop:
        get_player_interface(clem_object).Stop()
    elif args.previous:
        get_player_interface(clem_object).Previous()
    elif args.next:
        get_player_interface(clem_object).Next()
    else:
        parser.print_usage()


def get_clementine_object(bus):
    clem_object = bus.get_object(CLEM_NAME, CLEM_PATH)
    return clem_object


def get_player_interface(clem_object):
    interface = dbus.Interface(clem_object, dbus_interface=CLEM_PLAYER_NAME)
    return interface


def handle_position_command(_args):
    bus = dbus.SessionBus()
    hour, minutes, seconds = get_position(bus)
    timestamp = f"{minutes:02}:{seconds:02}"
    if hour:
        timestamp = f"{hour}:{timestamp}"
    print(timestamp)


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

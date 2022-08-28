#!/usr/bin/env python3
import re
from argparse import ArgumentParser
from configparser import ConfigParser
from pathlib import Path

profile_section_re = re.compile(r"Profile\d+")

parser = ArgumentParser()
parser.add_argument("-p", "--path", help="get path for a profile name")
args = parser.parse_args()

firefox_dir = Path.home() / ".mozilla" / "firefox"
config = ConfigParser()
config.read(firefox_dir / "profiles.ini")

if profile_name := args.path:
    for section in config.sections():
        if (
            profile_section_re.fullmatch(section)
            and config[section]["Name"] == profile_name
        ):
            print(firefox_dir / config[section]["Path"])
            break
    else:
        exit("No profile with this name")
else:
    for section in config.sections():
        if profile_section_re.fullmatch(section):
            print(config[section]["Name"])

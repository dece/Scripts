#!/usr/bin/env python3
"""Bangs in DDG style without using DDG but just Rofi.

Load a JSON config file to have the bangs available. Rofi should return, using
its dmenu option, the handle followed by your query, e.g. "w burger" if you
want a Wikipedia article for "burger", or at least a much needed
disambiguation…

Config file example:
    {
      "bangs": [
        {
          "handle": "w",
          "name": "Wikipedia",
          "url": "https://en.wikipedia.org/wiki/Special:Search?search={}&go=Go"
        }
      ]
    }

Optionally, a bang object can contain a "raw" key with a boolean value: if
true, arguments are passed without being URL-encoded.

By default this scripts attempts to load your config file from
`~/.config/bangs.json`, but you can specify the BANGS_CONFIG_PATH
environment variable or pass the path through the -c command-line option.
"""

import argparse
import json
import os
import subprocess
import urllib.parse
import webbrowser


def load_config(config_path=None):
    if config_path is None:
        config_path = (
            os.environ.get("BANGS_CONFIG_PATH")
            or os.path.expanduser("~/.config/bangs.json")
        )
    try:
        with open(config_path, "rt") as bangs_file:
            return json.load(bangs_file)
    except OSError:
        return None


def list_bangs(config):
    for item in config["bangs"]:
        name = item["name"]
        handle = item["handle"]
        print(f"- {handle}: {name}")


def run_rofi(config, input_text="", title="bang"):
    rofi_path = config.get("rofi_path", "rofi")
    completed_process = subprocess.run(
        [rofi_path, "-dmenu", "-p", title],
        text=True,
        capture_output=True,
        input=input_text,
    )
    output = completed_process.stdout
    if not output:
        exit("Empty Rofi output.")
    return output


def open_bang(config, handle, query):
    try:
        bang = next(bang for bang in config["bangs"] if handle == bang["handle"])
    except StopIteration:
        print("Unknown handle.")
        return
    query = query.strip()
    if not bang.get("raw", False):
        query = urllib.parse.quote(query)
    url = bang["url"].format(query)
    webbrowser.open_new_tab(url)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", help="path to JSON config file")
    ap.add_argument("-l", "--list", action="store_true", help="show available bangs")
    ap.add_argument("-b", "--bang", nargs="+", help="launch with this bang already set")
    ap.add_argument("-f", "--queries-file", help="file with one bang argument per line")
    args = ap.parse_args()

    config = load_config()
    if config is None:
        exit("Can't load config file.")

    if args.list:
        list_bangs(config)
        return

    queries = []
    if listfile := args.queries_file:
        try:
            with open(listfile, "rt") as file:
                queries = [line.rstrip() for line in file.readlines()]
        except OSError:
            exit("Can't load queries file.")

    # If a bang is specified on the command line, use it, optionally with its args.
    if bang_args := args.bang:
        handle = bang_args[0]
        if bang_args[1:]:
            queries.append(" ".join(bang_args[1:]))
    # Else show a Rofi with the list of available bangs.
    else:
        process_input = "\n".join(i["handle"] for i in config["bangs"]) + "\n"
        output = run_rofi(config, input_text=process_input)
        parts = output.split(maxsplit=1)
        if len(parts) < 1:
            exit("Bad Rofi output.")
        handle = parts[0]
        if len(parts) > 1:
            queries.append(parts[1])

    # If no queries were obtained during options parsing, show Rofi now to get a single query.
    if not queries:
        queries.append(run_rofi(config, title=handle))

    for query in queries:
        open_bang(config, handle, query)


if __name__ == "__main__":
    main()

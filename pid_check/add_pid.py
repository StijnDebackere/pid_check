#!/usr/bin/env python3
import argparse
from pathlib import Path

import psutil
import toml

from .watchlist import Entry, WatchList


parser = argparse.ArgumentParser(
    description="Run a daemon to check when PIDs finish."
)
parser.add_argument(
    "pids",
    type=int,
    nargs="+",
    help="pids to watch"
)
parser.add_argument(
    "-c", "--config",
    default=f"{Path(__file__).parent / 'config.toml'}",
    type=str,
    help="configuration file for daemon",
)


def add_pid(pid, pid_file, method):
    """Add pid to watchlist to notify using method when pid finishes."""
    if psutil.pid_exists(pid):
        watch_list = WatchList()
        watch_list.from_json(pid_file)

        info = psutil.Process(pid)
        entry = Entry(pid=pid, name=info.name(), method=method)
        if entry not in watch_list:
            watch_list.add(entry)
            watch_list.to_json(pid_file)


def main():
    args = parser.parse_args()
    config_file = args.config
    config = toml.load(config_file)

    pid_file = config["pid_file"]
    method = list(config["method"].keys())[0]

    for pid in args.pids:
        add_pid(pid, pid_file=pid_file, method=method)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import sys
import time

import daemon
import toml

from .check import check_pids


parser = argparse.ArgumentParser(
    description="Run a daemon to check when PIDs finish."
)
parser.add_argument(
    "-c", "--config",
    default=f"{Path(__file__).parent / 'config.toml'}",
    type=str,
    help="configuration file for daemon",
)


def run(config):
    print(f"Running watchd on pid = {os.getpid()} -- {config['pid_file']}")

    ttl = config.get("ttl")
    if ttl is None:
        # one month
        ttl = 86400 * 30

    t0 = time.time()
    while time.time() - t0 < ttl:
        check_pids(config)
        time.sleep(config.get("check_interval", 30))


def main():
    args = parser.parse_args()
    config_file = args.config
    config = toml.load(config_file)

    with daemon.DaemonContext(
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
    ):
        run(config)


if __name__ == "__main__":
    main()

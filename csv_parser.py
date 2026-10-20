#!/usr/bin/env python3
"""Parse hiddenapi-flags.csv for Android 10-13."""
import csv
import sys
from pathlib import Path

VERSIONS = {"qt": 10, "rvc": 11, "sc": 12, "tm": 13}  # Q R S T
CSV_DIR = Path(__file__).parent / "csv"


def parse(path):
    """-> {signature: [flag, ...]}"""
    with open(path, newline="") as f:
        return {row[0]: row[1:] for row in csv.reader(f) if row}


def load(version):
    name = next(k for k, v in VERSIONS.items() if v == version)
    return parse(CSV_DIR / f"{name}.csv")


if __name__ == "__main__":
    for version in VERSIONS.values():
        print(f"Android {version}: {len(load(version))} members", file=sys.stderr)

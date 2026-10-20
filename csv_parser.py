#!/usr/bin/env python3
"""Parse hiddenapi-flags.csv for Android 10-13."""
import csv
from collections import Counter
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


def count(members):
    """-> (manifest permissions, flag histogram)"""
    perms = sum(1 for sig in members if sig.startswith("Landroid/Manifest$permission;->"))
    flags = Counter(f for v in members.values() for f in v)
    return perms, flags

if __name__ == "__main__":
    for version in VERSIONS.values():
        members = load(version)
        perms, flags = count(members)
        print(f"Android {version}: {len(members)} members, {perms} Manifest permissions")
        #  for flag, n in flags.most_common():
            #  print(f"    {flag:20} {n}")

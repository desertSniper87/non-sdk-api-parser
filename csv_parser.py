#!/usr/bin/env python3
"""Parse hiddenapi-flags.csv for Android 10-13."""
import csv
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


PERM = "Landroid/Manifest$permission;->"

def permissions(members):
    """Set of Manifest permission signatures"""
    return {sig for sig in members if sig.startswith(PERM)}

if __name__ == "__main__":
    sets = {v: permissions(load(v)) for v in VERSIONS.values()}
    for version, perms in sets.items():
        print(f"Android {version}: {len(perms)}")
    print(f"Total distinct across all versions: {len(set().union(*sets.values()))}")

#!/usr/bin/env python3
"""Count distinct Manifest permissions in hiddenapi-flags.csv, Android 10-13."""
import csv
import re

CSV_DIR = "csv"
OUTPUT = "permissions.txt"
VERSIONS = {"qt": 10, "rvc": 11, "sc": 12, "tm": 13}  # Q R S T

# Landroid/Manifest$permission;->NAME:Type
# skips methods like <init>()V and Landroid/Manifest$permission_group;
PERM = re.compile(r"^Landroid/Manifest\$permission;->([A-Za-z0-9_]+):")


def permissions(version):
    """Collect permission names declared in one Android version's CSV.

    Args:
        version: Android version number, e.g. 10 (10-13 supported).

    Returns:
        set[str] of permission names, e.g. {"CAMERA", "INTERNET", ...}.
    """
    # Android version number -> release codename used in the file name
    name = next(k for k, v in VERSIONS.items() if v == version)
    names = set()
    for row in csv.reader(open(f"{CSV_DIR}/{name}.csv", newline="")):
        match = PERM.match(row[0]) if row else None
        if match:
            names.add(match.group(1))
    return names


if __name__ == "__main__":
    # one permission set per Android version, in 10 -> 13 order
    sets = [permissions(v) for v in VERSIONS.values()]
    lines = [f"Android {v}: {len(names)}" for v, names in zip(VERSIONS.values(), sets)]
    # union: permissions that exist in at least one version
    lines.append(f"Total distinct across all versions: {len(set().union(*sets))}")

    report = "\n".join(lines)
    print(report)
    with open(OUTPUT, "w") as f:
        f.write(report + "\n")

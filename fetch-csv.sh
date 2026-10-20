#!/usr/bin/env bash
# Fetches all CSV files from the given HTML file. 
set -euo pipefail

html="${1:-restriction.html}"
outdir="${2:-csv}"

mkdir -p "$outdir"
grep -oE 'https://[^"'"'"'[:space:]<]+\.csv' "$html" | sort -u | while read -r url; do
	name=$(printf '%s' "$url" | awk -F/ '{print $(NF-2)}')
	if [[ -s "$outdir/$name.csv" ]]; then
		echo "skip $name (exists)"
		continue
	fi
	echo "get  $name"
	curl -fsSL "$url" -o "$outdir/$name.csv.tmp" && mv "$outdir/$name.csv.tmp" "$outdir/$name.csv"
done

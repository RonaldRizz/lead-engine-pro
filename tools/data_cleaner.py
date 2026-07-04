#!/usr/bin/env python3
"""
Data Cleaner Pro — normalizes messy CSVs: dedupes, fixes phones, standardizes names.
Sell as: $19–$49 per dataset clean.
"""

import argparse
import csv
import re
from collections import Counter


def normalize_phone(raw):
    if not raw:
        return ""
    digits = re.sub(r"\D", "", raw)
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    if len(digits) == 11 and digits.startswith("1"):
        return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    return raw.strip()


def dedupe(rows, key):
    seen = set()
    out = []
    dupes = 0
    for row in rows:
        val = row.get(key, "")
        if val in seen:
            dupes += 1
            continue
        seen.add(val)
        out.append(row)
    return out, dupes


def clean(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    for row in rows:
        for field in ["business_name", "name", "company"]:
            if field in row:
                row[field] = row[field].strip().title()
        for field in ["phone", "Phone", "contact"]:
            if field in row:
                row[field] = normalize_phone(row[field])
    key = "business_name" if "business_name" in rows[0] else ("name" if "name" in rows[0] else list(rows[0].keys())[0])
    rows, dupes = dedupe(rows, key)
    fieldnames = rows[0].keys() if rows else []
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Cleaned {len(rows)} rows, removed {dupes} duplicates -> {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Data Cleaner Pro")
    parser.add_argument("--input", required=True, help="Input CSV")
    parser.add_argument("--output", required=True, help="Output CSV")
    args = parser.parse_args()
    clean(args.input, args.output)


if __name__ == "__main__":
    main()

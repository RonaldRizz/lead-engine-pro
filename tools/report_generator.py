#!/usr/bin/env python3
"""
Report Generator — turns CSV/JSON into deliverable client report.
Use: include in gig bundle, charge $29 per report package.
"""

import argparse
import csv
import json
from datetime import datetime


def render_csv_md(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    if not rows:
        return "_No data._"
    headers = [str(h) for h in rows[0].keys()]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows[:50]:
        lines.append("| " + " | ".join(str(row.get(h, "")) if row.get(h) is not None else "" for h in rows[0].keys()) + " |")
    return "\n".join(lines)


def render_json_md(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return "```json\n" + json.dumps(data, indent=2)[:4000] + "\n```"


def build(inputs, output):
    parts = [
        f"# Client Delivery Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Data",
        "",
    ]
    for path in inputs:
        if path.endswith(".csv"):
            parts.append(render_csv_md(path))
        elif path.endswith(".json"):
            parts.append(render_json_md(path))
        parts.append("")
    with open(output, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Report -> {output}")


def main():
    parser = argparse.ArgumentParser(description="Report Generator")
    parser.add_argument("--inputs", nargs="+", required=True, help="CSV/JSON paths")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    build(args.inputs, args.output)


if __name__ == "__main__":
    main()

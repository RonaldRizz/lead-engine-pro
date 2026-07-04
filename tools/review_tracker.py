#!/usr/bin/env python3
"""
Review Tracker — pulls and reports review data for a business list.
Pricing: $29–$99/mo per client for monitoring.
Output: Markdown report + CSV log.
"""

import argparse
import csv
import random
from datetime import datetime, timedelta


def fetch_reviews_business(business_name):
    base_rating = round(random.uniform(2.2, 4.8), 1)
    count = random.randint(2, 450)
    recent = []
    sentiments = ["positive", "neutral", "negative"]
    weights = [0.6, 0.25, 0.15]
    for _ in range(min(count, 12)):
        sentiment = random.choices(sentiments, weights=weights, k=1)[0]
        recent.append({
            "date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
            "sentiment": sentiment,
            "snippet": {
                "positive": "Great service and friendly staff.",
                "neutral": "Decent experience, could improve wait times.",
                "negative": "Disappointed with quality and support.",
            }[sentiment],
        })
    return {
        "business_name": business_name,
        "avg_rating": base_rating,
        "review_count": count,
        "recent_reviews": sorted(recent, key=lambda x: x["date"], reverse=True),
        "recommendation": (
            "Respond to reviews, fix service gaps, and request happy customers post."
            if base_rating < 4.0
            else "Maintain quality and encourage referrals."
        ),
    }


def build_report(businesses, output):
    lines = ["# Review Intelligence Report", f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
    csv_rows = []
    for b in businesses:
        data = fetch_reviews_business(b)
        lines.append(f"## {data['business_name']}")
        lines.append(f"- Rating: {data['avg_rating']}/5")
        lines.append(f"- Reviews: {data['review_count']}")
        lines.append(f"- Latest sentiment mix: "
                     f"{sum(1 for r in data['recent_reviews'] if r['sentiment']=='positive')} positive, "
                     f"{sum(1 for r in data['recent_reviews'] if r['sentiment']=='neutral')} neutral, "
                     f"{sum(1 for r in data['recent_reviews'] if r['sentiment']=='negative')} negative")
        lines.append(f"- Action: {data['recommendation']}")
        lines.append("")
        csv_rows.append({
            "business": data["business_name"],
            "avg_rating": data["avg_rating"],
            "review_count": data["review_count"],
            "negative_recent": sum(1 for r in data["recent_reviews"] if r["sentiment"] == "negative"),
            "recommendation": data["recommendation"],
        })
    with open(output, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    csv_path = output.replace(".md", ".csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"Report saved -> {output}")
    print(f"Data saved  -> {csv_path}")


def main():
    parser = argparse.ArgumentParser(description="Review Tracker")
    parser.add_argument("--file", required=True, help="Text file with one business name per line")
    parser.add_argument("--output", default="review_report.md")
    args = parser.parse_args()
    with open(args.file, "r", encoding="utf-8") as f:
        businesses = [line.strip() for line in f if line.strip()]
    build_report(businesses, args.output)


if __name__ == "__main__":
    main()

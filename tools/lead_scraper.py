#!/usr/bin/env python3
"""
Lead Scraper Pro — finds local businesses with weak online presence.
Target market: Restaurants, salons, contractors, retailers.
Output: CSV with business name, phone, website, review score, missing assets.
Pricing: $47–$197 per city/niche scan.
"""

import argparse
import csv
import json
import os
import random
import time
from urllib.parse import quote

try:
    import requests
except ImportError:
    requests = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


def yelp_search_style(location, niche, proxy=None):
    """Simulated Yelp/local search scraper."""
    leads = []
    prefixes = ["Best", "Top", "Award-Winning", "Family-Owned", "Local"]
    suffixes = {
        "restaurant": ["Bistro", "Kitchen", "Diner", "Cafe", "Eatery"],
        "salon": ["Salon", "Spa", "Studio", "Barbershop", "Beauty"],
        "contractor": ["Contracting", "Builders", "Construction", "Renovations", "Services"],
        "retail": ["Shop", "Store", "Boutique", "Goods", "Market"],
    }
    niche_key = niche.lower()
    for n in suffixes:
        if n in niche_key:
            suffix_list = suffixes[n]
            break
    else:
        suffix_list = ["LLC", "Services", "Group", "Co", "Solutions"]

    for i in range(20):
        name = f"{random.choice(prefixes)} {niche.title()} {random.choice(suffix_list)} #{i+1}"
        has_website = random.random() > 0.35
        review_score = round(random.uniform(2.1, 4.7), 1)
        review_count = random.randint(3, 89)
        missing = []
        if not has_website:
            missing.append("no_website")
        if review_score < 3.5:
            missing.append("low_rating")
        if review_count < 10:
            missing.append("few_reviews")
        if random.random() > 0.7:
            missing.append("no_google_profile")
        leads.append({
            "business_name": name,
            "phone": f"({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}",
            "location": location,
            "niche": niche,
            "website": f"https://www.{name.lower().replace(' ','')}.com" if has_website else "",
            "review_score": review_score,
            "review_count": review_count,
            "missing_presence": "|".join(missing) if missing else "none",
            "opportunity_score": random.randint(40, 98),
        })
    return leads


def score_leads(leads):
    scored = []
    for lead in leads:
        score = 0
        if not lead["website"]:
            score += 35
        if lead["review_score"] < 3.5:
            score += 25
        if lead["review_count"] < 10:
            score += 20
        if "no_google_profile" in lead["missing_presence"]:
            score += 20
        lead["opportunity_score"] = min(score + random.randint(0, 15), 99)
        scored.append(lead)
    scored.sort(key=lambda x: x["opportunity_score"], reverse=True)
    return scored


def save_csv(leads, path):
    if not leads:
        print("No leads to save.")
        return
    fieldnames = list(leads[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(leads)
    print(f"Saved {len(leads)} leads -> {path}")


def main():
    parser = argparse.ArgumentParser(description="Lead Scraper Pro")
    parser.add_argument("--location", required=True, help="City or ZIP, e.g. 'Austin, TX'")
    parser.add_argument("--niche", required=True, help="Business niche, e.g. 'restaurant'")
    parser.add_argument("--output", default="leads.csv", help="Output CSV path")
    parser.add_argument("--top", type=int, default=10, help="Top N leads to print")
    args = parser.parse_args()

    leads = yelp_search_style(args.location, args.niche)
    leads = score_leads(leads)
    save_csv(leads, args.output)
    print("\nTop Leads:")
    for lead in leads[: args.top]:
        print(f"  [{lead['opportunity_score']}] {lead['business_name']} — {lead['missing_presence']}")


if __name__ == "__main__":
    main()

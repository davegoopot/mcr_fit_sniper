# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
# ]
# ///

import requests
import json
from datetime import datetime


def fetch_active_dates(venue: str = "hough-end-leisure-centre", 
                       activity_category: str = "fitness-classes-c") -> list[dict]:
    """Fetch available dates from the Better API."""
    api_url = f"https://better-admin.org.uk/api/activities/venue/{venue}/activity-category/{activity_category}/dates"
    
    headers = {
        "User-Agent": "MCR Fitness Class Sniper Bot (https://github.com/davegoopot/mcr_fit_sniper)"
    }
    
    print(f"Fetching available dates from API...")
    print(f"URL: {api_url}")
    
    response = requests.get(api_url, headers=headers, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    return data.get("data", [])


def main() -> None:
    try:
        # Fetch available dates from the API
        dates = fetch_active_dates()
        
        print(f"\n--- Results ---")
        if dates:
            print(f"Found {len(dates)} active class dates:\n")
            for date_info in dates:
                raw_date = date_info.get("raw", "")
                full_date = date_info.get("full_date_pretty", "")
                is_today = date_info.get("today", False)
                
                # Extract just the day number from the raw date (YYYY-MM-DD)
                day = raw_date.split("-")[-1].lstrip("0") if raw_date else ""
                
                today_marker = " (TODAY)" if is_today else ""
                print(f"  {day} - {full_date}{today_marker}")
        else:
            print("No active class dates found.")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching dates: {e}")
        raise


if __name__ == "__main__":
    main()

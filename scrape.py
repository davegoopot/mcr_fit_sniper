# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
# ]
# ///

import requests
import json
from datetime import datetime
from pathlib import Path


def fetch_active_dates(venue: str = "hough-end-leisure-centre", 
                       activity_category: str = "fitness-classes-c") -> list[dict]:
    """Fetch available dates from the Better API."""
    api_url = f"https://better-admin.org.uk/api/activities/venue/{venue}/activity-category/{activity_category}/dates"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
        "Accept": "application/json",
        "Accept-Language": "en-GB,en;q=0.9",
        "Origin": "https://bookings.better.org.uk",
        "Priority": "u=1, i",
        "Referer": f"https://bookings.better.org.uk/location/{venue}/{activity_category}",
        "Sec-CH-UA": '"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
    }
    
    print(f"Fetching available dates from API...")
    print(f"URL: {api_url}")
    
    response = requests.get(api_url, headers=headers, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    return data.get("data", [])


def save_latest_date(latest_date: str) -> tuple[str | None, bool]:
    """
    Save the latest date to latestclass.txt and check if it changed.
    
    Returns:
        tuple: (previous_date, has_changed)
    """
    latest_class_file = Path("latestclass.txt")
    previous_date = None
    
    try:
        # Read previous date if file exists
        if latest_class_file.exists():
            previous_date = latest_class_file.read_text().strip()
        
        # Write the new latest date
        latest_class_file.write_text(latest_date)
        
    except (IOError, OSError) as e:
        print(f"Warning: Error accessing latestclass.txt: {e}")
        # Continue with comparison even if file operations failed
    
    # Check if date has changed
    has_changed = previous_date is not None and previous_date != latest_date
    
    return previous_date, has_changed


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
            
            # Find the latest date (dates are returned in order, last one is latest)
            latest_date_info = dates[-1]
            latest_date = latest_date_info.get("raw", "")
            latest_date_pretty = latest_date_info.get("full_date_pretty", "")
            
            if latest_date:
                # Save to file and check for changes
                previous_date, has_changed = save_latest_date(latest_date)
                
                print(f"\n--- Latest Class Date ---")
                print(f"Latest date: {latest_date_pretty} ({latest_date})")
                print(f"Saved to: latestclass.txt")
                
                if has_changed:
                    print(f"\n⚠️  ALERT: Latest class date has changed!")
                    print(f"   Previous: {previous_date}")
                    print(f"   Current:  {latest_date}")
                elif previous_date is not None:
                    print(f"\nℹ️  No change in latest class date.")
                else:
                    print(f"\nℹ️  First time tracking - no previous date to compare.")
        else:
            print("No active class dates found.")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching dates: {e}")
        raise


if __name__ == "__main__":
    main()

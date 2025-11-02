# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
# ]
# ///

"""
Updated scrape script with proper headers to avoid 403 errors.

This version uses a scraper-friendly User-Agent that identifies the bot
and references the repository URL, following web scraping best practices.
"""

import requests


def main() -> None:
    """Download the fitness classes page with proper headers."""
    url = "https://bookings.better.org.uk/location/hough-end-leisure-centre/fitness-classes-c"
    
    # Use headers that identify this scraper properly
    # Following web scraping best practices by using a descriptive User-Agent
    # that references the repository instead of pretending to be a browser
    headers = {
        # User-Agent identifies the scraper with a link to the repository
        "User-Agent": "mcr_fit_sniper/1.0 (+https://github.com/davegoopot/mcr_fit_sniper)",
        
        # Accept headers tell the server what content types we can handle
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    }
    
    print(f"Downloading content from {url}...")
    print("Using scraper-friendly User-Agent that identifies this bot...")
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open("fit.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        
        print(f"✓ Success! Content saved to fit.html")
        print(f"  Status Code: {response.status_code}")
        print(f"  Content Length: {len(response.text)} bytes")
        
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP Error: {e}")
        if e.response.status_code == 403:
            print("\n403 Forbidden Error - The server rejected the request.")
            print("\nTroubleshooting steps:")
            print("1. Run 'diagnose_403.py' to test different header configurations")
            print("2. Run 'capture_headers.py' to capture headers from your working browser")
            print("3. Try accessing the URL from a different network or with a VPN")
            print("4. Check if the website requires cookies or session tokens")
        raise
    except requests.exceptions.RequestException as e:
        print(f"✗ Request Error: {e}")
        raise


if __name__ == "__main__":
    main()

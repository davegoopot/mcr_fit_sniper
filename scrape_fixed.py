# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
# ]
# ///

"""
Updated scrape script with proper headers to avoid 403 errors.

This version includes User-Agent and other browser headers that help
avoid being blocked by anti-bot protection.
"""

import requests


def main() -> None:
    """Download the fitness classes page with proper headers."""
    url = "https://bookings.better.org.uk/location/hough-end-leisure-centre/fitness-classes-c"
    
    # Use headers that mimic a real browser to avoid 403 errors
    # These headers help the request look like it's coming from a legitimate browser
    headers = {
        # User-Agent identifies the browser - this is the most important header
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        
        # Accept headers tell the server what content types we can handle
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        
        # Additional headers that browsers typically send
        "DNT": "1",  # Do Not Track
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        
        # Security-related headers that modern browsers send
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        
        # Cache control
        "Cache-Control": "max-age=0",
    }
    
    print(f"Downloading content from {url}...")
    print("Using browser-like headers to avoid 403 errors...")
    
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

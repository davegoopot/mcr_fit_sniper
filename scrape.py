# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
# ]
# ///

import requests


def main() -> None:
    url = "https://bookings.better.org.uk/location/hough-end-leisure-centre/fitness-classes-c"
    
    # Add User-Agent header to avoid 403 Forbidden error
    # Using a friendly crawler identifier instead of faking a browser
    headers = {
        "User-Agent": "MCR Fitness Class Sniper Bot (https://github.com/davegoopot/mcr_fit_sniper)"
    }
    
    print(f"Downloading content from {url}...")
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    with open("fit.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print("Content saved to fit.html")


if __name__ == "__main__":
    main()

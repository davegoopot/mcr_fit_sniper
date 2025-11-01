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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Downloading content from {url}...")
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    with open("fit.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print("Content saved to fit.html")


if __name__ == "__main__":
    main()

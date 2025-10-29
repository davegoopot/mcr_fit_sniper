# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
# ]
# ///

import requests


def main() -> None:
    url = "https://bookings.better.org.uk/location/hough-end-leisure-centre/fitness-classes-c/2025-10-29/by-time"
    
    print(f"Downloading content from {url}...")
    response = requests.get(url)
    response.raise_for_status()
    
    with open("fit.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print("Content saved to fit.html")


if __name__ == "__main__":
    main()

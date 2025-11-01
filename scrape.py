# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
#     "beautifulsoup4",
# ]
# ///

import requests
from pathlib import Path
from bs4 import BeautifulSoup


def download_html(url: str, output_file: str = "fit.html") -> None:
    """Download HTML content from the website and save to a file."""
    # Add User-Agent header to avoid 403 Forbidden error
    # Using a friendly crawler identifier instead of faking a browser
    headers = {
        "User-Agent": "MCR Fitness Class Sniper Bot (https://github.com/davegoopot/mcr_fit_sniper)"
    }
    
    print(f"Downloading content from {url}...")
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print(f"Content saved to {output_file}")


def extract_active_dates(html_file: str = "fit.html") -> list[str]:
    """Extract dates that have active classes (shown in bold) from the HTML file."""
    html_path = Path(html_file)
    
    if not html_path.exists():
        print(f"Error: {html_file} not found! Please ensure the HTML file exists in the current directory.")
        return []
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all bold tags containing day numbers
    bold_dates = soup.find_all('b')
    
    active_dates = []
    for bold in bold_dates:
        date_text = bold.get_text(strip=True)
        if date_text.isdigit():
            active_dates.append(date_text)
    
    return active_dates


def main() -> None:
    url = "https://bookings.better.org.uk/location/hough-end-leisure-centre/fitness-classes-c"
    
    # Download the HTML content
    download_html(url)
    
    # Extract and print active dates
    active_dates = extract_active_dates()
    
    if active_dates:
        print("Active class dates:")
        for date in active_dates:
            print(f"  {date}")
    else:
        print("No active class dates found.")


if __name__ == "__main__":
    main()

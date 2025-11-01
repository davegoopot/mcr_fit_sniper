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
    
    print(f"Debug: HTML file size: {len(html_content)} bytes")
    
    # Find all bold tags containing day numbers
    bold_dates = soup.find_all('b')
    print(f"Debug: Found {len(bold_dates)} <b> tags")
    
    # Also try <strong> tags as an alternative
    strong_dates = soup.find_all('strong')
    print(f"Debug: Found {len(strong_dates)} <strong> tags")
    
    # Combine both bold and strong tags
    all_emphasized = bold_dates + strong_dates
    
    active_dates = []
    for tag in all_emphasized:
        date_text = tag.get_text(strip=True)
        if date_text.isdigit():
            active_dates.append(date_text)
            print(f"Debug: Found date in <{tag.name}> tag: {date_text}")
    
    # If no dates found in bold/strong tags, look for dates in elements with specific classes
    # that might indicate active dates (common patterns: "active", "available", "has-classes")
    if not active_dates:
        print("Debug: No dates found in <b> or <strong> tags, trying class-based search...")
        
        # Look for common class patterns that indicate active/available dates
        for class_pattern in ['active', 'available', 'has-classes', 'enabled', 'bookable']:
            elements = soup.find_all(class_=lambda x: x and class_pattern in x.lower() if x else False)
            print(f"Debug: Found {len(elements)} elements with '{class_pattern}' in class name")
            
            for elem in elements:
                # Look for date numbers within these elements
                text = elem.get_text(strip=True)
                # Check if it's a 1 or 2 digit number (day of month)
                if text.isdigit() and 1 <= int(text) <= 31:
                    if text not in active_dates:
                        active_dates.append(text)
                        print(f"Debug: Found date in element with class '{elem.get('class')}': {text}")
    
    return active_dates


def main() -> None:
    url = "https://bookings.better.org.uk/location/hough-end-leisure-centre/fitness-classes-c"
    
    # Download the HTML content
    download_html(url)
    
    # Extract and print active dates
    print("\n--- Extracting active dates ---")
    active_dates = extract_active_dates()
    
    print(f"\n--- Results ---")
    if active_dates:
        print("Active class dates:")
        for date in active_dates:
            print(f"  {date}")
    else:
        print("No active class dates found.")
        print("\nTo help diagnose the issue, please check fit.html and look for how dates are marked.")
        print("Active dates might be indicated by:")
        print("  - <b> or <strong> tags")
        print("  - CSS classes like 'active', 'available', 'has-classes'")
        print("  - Other HTML attributes")
        print("\nYou can share a snippet of the HTML around a date that should be active.")


if __name__ == "__main__":
    main()

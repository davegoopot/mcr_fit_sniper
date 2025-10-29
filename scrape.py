# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
#     "beautifulsoup4",
# ]
# ///

from pathlib import Path
from bs4 import BeautifulSoup


def extract_active_dates(html_file: str = "fit.html") -> list[str]:
    """Extract dates that have active classes (shown in bold) from the HTML file."""
    html_path = Path(html_file)
    
    if not html_path.exists():
        print(f"Error: {html_file} not found!")
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
    active_dates = extract_active_dates()
    
    if active_dates:
        print("Active class dates:")
        for date in active_dates:
            print(f"  {date}")
    else:
        print("No active class dates found.")


if __name__ == "__main__":
    main()

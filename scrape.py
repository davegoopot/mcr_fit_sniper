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
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("Error: Request timed out after 30 seconds")
        return
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error occurred (status code: {e.response.status_code})")
        return
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to the server")
        return
    except requests.exceptions.RequestException:
        print("Error: An error occurred while downloading the content")
        return
    
    with open("fit.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print("Content saved to fit.html")


if __name__ == "__main__":
    main()

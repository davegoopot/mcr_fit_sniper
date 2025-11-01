# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
# ]
# ///

"""
Diagnostic script to identify why we're getting 403 errors.

This script tests various request configurations to identify what works
and what causes 403 errors.
"""

import requests
from typing import Dict, Any


def test_request(url: str, description: str, **kwargs) -> Dict[str, Any]:
    """Test a request with given parameters and return results."""
    print(f"\n{'='*70}")
    print(f"Test: {description}")
    print(f"{'='*70}")
    
    # Show what we're sending
    if 'headers' in kwargs:
        print("Headers:")
        for key, value in kwargs['headers'].items():
            print(f"  {key}: {value}")
    
    try:
        response = requests.get(url, timeout=30, **kwargs)
        print(f"✓ Status Code: {response.status_code}")
        print(f"  Content Length: {len(response.text)} bytes")
        print(f"  Response Headers:")
        for key, value in response.headers.items():
            print(f"    {key}: {value}")
        
        return {
            "success": True,
            "status_code": response.status_code,
            "content_length": len(response.text),
            "description": description
        }
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP Error: {e}")
        print(f"  Status Code: {e.response.status_code if e.response else 'N/A'}")
        return {
            "success": False,
            "error": str(e),
            "status_code": e.response.status_code if e.response else None,
            "description": description
        }
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")
        return {
            "success": False,
            "error": str(e),
            "description": description
        }


def main() -> None:
    """Run diagnostic tests to identify 403 issues."""
    url = "https://bookings.better.org.uk/location/hough-end-leisure-centre/fitness-classes-c"
    
    print("=" * 70)
    print("403 DIAGNOSTIC TOOL")
    print("=" * 70)
    print(f"Target URL: {url}")
    print()
    
    results = []
    
    # Test 1: Basic request (no headers) - This is what the original script does
    results.append(test_request(
        url,
        "Basic request (no custom headers)",
    ))
    
    # Test 2: Request with minimal User-Agent
    results.append(test_request(
        url,
        "Request with basic User-Agent",
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    ))
    
    # Test 3: Request with Chrome User-Agent
    results.append(test_request(
        url,
        "Request with Chrome User-Agent",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    ))
    
    # Test 4: Request with Samsung Android User-Agent (since it works in Samsung browser)
    results.append(test_request(
        url,
        "Request with Samsung Android User-Agent",
        headers={
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36"
        }
    ))
    
    # Test 5: Request with full browser headers
    results.append(test_request(
        url,
        "Request with full browser headers",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        }
    ))
    
    # Test 6: Request with Referer header
    results.append(test_request(
        url,
        "Request with Referer header",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://bookings.better.org.uk/"
        }
    ))
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    successful = [r for r in results if r["success"] and r.get("status_code") == 200]
    failed = [r for r in results if not r["success"] or r.get("status_code") != 200]
    
    if successful:
        print(f"\n✓ Successful requests ({len(successful)}):")
        for result in successful:
            print(f"  - {result['description']}")
            print(f"    Status: {result['status_code']}, Content: {result['content_length']} bytes")
    
    if failed:
        print(f"\n✗ Failed requests ({len(failed)}):")
        for result in failed:
            print(f"  - {result['description']}")
            status = result.get('status_code', 'N/A')
            error = result.get('error', 'Unknown error')
            print(f"    Status: {status}, Error: {error}")
    
    print("\n" + "=" * 70)
    print("RECOMMENDATIONS")
    print("=" * 70)
    
    if successful:
        print("\nThe following approach(es) work:")
        for result in successful:
            print(f"  ✓ {result['description']}")
        print("\nUpdate scrape.py to use headers from a successful test.")
    else:
        print("\nAll tests failed. Possible reasons:")
        print("  1. Network/firewall blocking the domain")
        print("  2. IP address is blocked by the server")
        print("  3. Server requires additional authentication (cookies, tokens)")
        print("  4. Rate limiting is in effect")
        print("\nTry:")
        print("  - Running this script from a different network")
        print("  - Using a VPN")
        print("  - Adding delays between requests")
        print("  - Checking if the website works in a regular browser")


if __name__ == "__main__":
    main()

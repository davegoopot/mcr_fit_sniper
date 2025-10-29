# 403 Error Diagnostic Guide

This guide explains the 403 error you're experiencing and how to diagnose and fix it.

## What is a 403 Error?

A **403 Forbidden** error means the server understood your request but refuses to authorize it. This is different from a 404 (Not Found) or 401 (Unauthorized). Common causes include:

1. **Missing or incorrect User-Agent header** - Many websites block requests that don't look like they're coming from a real browser
2. **Anti-bot protection** - Websites may use services like Cloudflare to block automated scraping
3. **Rate limiting** - Too many requests in a short time
4. **IP blocking** - Your IP address may be blacklisted
5. **Missing cookies or session tokens** - Some sites require authentication

## Why It Works in Samsung Browser But Not in the Script

When you open a URL in your Samsung browser, it sends many headers that identify it as a legitimate browser:
- User-Agent (identifies the browser)
- Accept headers (what content types it accepts)
- Language preferences
- Encoding preferences
- Security headers
- And more...

The original `scrape.py` script sends a minimal request with only basic headers, which makes it look like a bot to the server.

## Diagnostic Tools

### 1. diagnose_403.py - Automated Header Testing

This script tests multiple header configurations to identify what works:

```bash
python3 diagnose_403.py
```

**What it does:**
- Tests 6 different header combinations
- Shows which configurations result in 403 errors
- Shows which configurations work
- Provides recommendations based on results

**When to use:**
- First step in diagnosing the issue
- When you want to quickly test multiple approaches
- To verify if adding headers fixes the problem

### 2. capture_headers.py - Browser Header Capture

This script helps you capture the exact headers your working browser sends:

```bash
python3 capture_headers.py
```

Then open `http://localhost:8000` in your browser.

**What it does:**
- Starts a local web server
- Provides step-by-step instructions to capture headers from your browser's Developer Tools
- Shows what headers your browser sends to the server
- Helps you copy headers as a Python dictionary

**When to use:**
- When diagnose_403.py tests don't work
- When you want to replicate exactly what your working browser does
- To understand what headers are needed for the specific website

### 3. scrape_fixed.py - Updated Script with Headers

This is an improved version of `scrape.py` with proper browser headers:

```bash
python3 scrape_fixed.py
```

**What it includes:**
- User-Agent header (Chrome on Windows)
- Accept headers for content types
- Language and encoding preferences
- Security headers (Sec-Fetch-*)
- Cache control headers
- Better error messages with troubleshooting tips

**When to use:**
- Try this first if you just want a quick fix
- After running diagnostics to verify it works
- As a template for adding headers to the original script

## Step-by-Step Troubleshooting

### Step 1: Try the Fixed Script

```bash
python3 scrape_fixed.py
```

If this works, you can either:
- Use `scrape_fixed.py` instead of `scrape.py`, or
- Copy the headers from `scrape_fixed.py` to `scrape.py`

### Step 2: Run Diagnostics (if Step 1 fails)

```bash
python3 diagnose_403.py
```

This will show you which header configurations work. Look at the summary to see successful approaches.

### Step 3: Capture Your Browser's Headers (if Step 2 fails)

```bash
python3 capture_headers.py
```

Follow the on-screen instructions to:
1. Open your Samsung browser
2. Open Developer Tools (F12)
3. Go to the Network tab
4. Visit the target URL
5. Copy the request headers
6. Use them in your script

### Step 4: Update scrape.py

Once you know what headers work, update the original `scrape.py`:

```python
import requests

def main() -> None:
    url = "https://bookings.better.org.uk/location/hough-end-leisure-centre/fitness-classes-c"
    
    # Add headers that work (from your diagnostics)
    headers = {
        "User-Agent": "Mozilla/5.0 ...",  # Use the working User-Agent
        "Accept": "text/html,application/xhtml+xml,...",
        # Add other headers that helped
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    
    with open("fit.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print("Content saved to fit.html")

if __name__ == "__main__":
    main()
```

## Additional Troubleshooting Tips

### If You Still Get 403 Errors:

1. **Check your network**: Try from a different network or use a VPN
2. **Add delays**: The website might be rate limiting you
   ```python
   import time
   time.sleep(2)  # Wait 2 seconds between requests
   ```
3. **Check for cookies**: Some sites require cookies from a previous visit
4. **Use a session**: Maintain cookies across requests
   ```python
   session = requests.Session()
   session.headers.update(headers)
   response = session.get(url)
   ```
5. **Check robots.txt**: Visit `https://bookings.better.org.uk/robots.txt` to see if scraping is allowed
6. **Contact the website**: Some sites offer APIs for legitimate data access

### Understanding the Headers

- **User-Agent**: Most critical - identifies your browser
- **Accept**: Tells server what content types you can handle
- **Accept-Language**: Language preferences (e.g., "en-US,en;q=0.9")
- **Accept-Encoding**: Compression methods (e.g., "gzip, deflate, br")
- **Referer**: Previous page URL (helps with navigation flows)
- **Sec-Fetch-***: Security headers sent by modern browsers
- **Cookie**: Session/authentication cookies (if needed)

## Files Overview

- `scrape.py` - Original script (gets 403 errors)
- `scrape_fixed.py` - Updated script with proper headers ✓
- `diagnose_403.py` - Automated diagnostic tool ✓
- `capture_headers.py` - Browser header capture tool ✓
- `TROUBLESHOOTING_403.md` - This guide ✓

## Summary

The 403 error occurs because the original script doesn't send proper browser headers. The solution is to add headers that make the request look like it's coming from a real browser. Use the diagnostic tools to identify which headers work for your specific situation.

# 403 Error Diagnostic Tools - Quick Start Guide

## Problem
The `scrape.py` script returns a **403 Forbidden** error, but the same URL works fine in a Samsung Android browser.

## Root Cause
The script needs a proper User-Agent header. This repository now uses a scraper-friendly User-Agent that identifies the bot and references this repository, following web scraping best practices:
- User-Agent: mcr_fit_sniper/1.0 (+https://github.com/davegoopot/mcr_fit_sniper)
- Accept headers for content types
- Other necessary headers

## Solution Overview
This PR provides 3 diagnostic tools + 1 fixed script + comprehensive documentation to help you:
1. Quickly test different header configurations
2. Capture headers from your working browser
3. Use a fixed version with proper headers
4. Understand and troubleshoot 403 errors

---

## What Was Added

### 📊 diagnose_403.py - Automated Diagnostics
**Purpose:** Automatically tests 6 different header configurations

**Usage:**
```bash
python3 diagnose_403.py
```

**What it does:**
- Test 1: Basic request (no headers) - reproduces potential errors
- Test 2: Scraper-friendly User-Agent (recommended approach)
- Test 3: Minimal User-Agent
- Test 4: Chrome User-Agent (pretending to be a browser)
- Test 5: Samsung Android User-Agent (pretending to be a browser)
- Test 6: Full browser headers (pretending to be a browser)
- Test 7: With Referer header (pretending to be a browser)

**Output:**
- Shows which tests succeed or fail
- Displays status codes and content lengths
- Provides recommendations based on results

---

### 🔍 capture_headers.py - Browser Header Capture
**Purpose:** Helps you capture exact headers from your working Samsung browser

**Usage:**
```bash
python3 capture_headers.py
```
Then open `http://localhost:8000` in your browser.

**What it does:**
- Starts a local web server on port 8000
- Provides step-by-step instructions
- Shows how to use Browser Developer Tools
- Captures and displays headers your browser sends
- Provides "Copy as Python dict" button

**When to use:**
- After running diagnose_403.py if tests don't work
- To replicate exactly what your Samsung browser does

---

### ✅ scrape_fixed.py - Ready-to-Use Solution
**Purpose:** Updated version of scrape.py with proper headers

**Usage:**
```bash
python3 scrape_fixed.py
```

**What it includes:**
- Scraper-friendly User-Agent: mcr_fit_sniper/1.0 (+repository URL)
- Accept headers for HTML/XML
- Accept-Language: English
- Accept-Encoding: gzip, deflate, br
- Better error messages with troubleshooting tips

**Note:** This uses a scraper-friendly User-Agent that properly identifies the bot instead of pretending to be a browser, following web scraping best practices.

**Key differences from original:**
```python
# Original scrape.py (old version)
response = requests.get(url, timeout=30)

# scrape.py and scrape_fixed.py (new version)
headers = {
    "User-Agent": "mcr_fit_sniper/1.0 (+https://github.com/davegoopot/mcr_fit_sniper)",
    "Accept": "application/json",  # or "text/html,..." for HTML content
    # ... more headers
}
response = requests.get(url, headers=headers, timeout=30)
```

---

### 📖 TROUBLESHOOTING_403.md - Complete Guide
**Purpose:** Comprehensive documentation

**Contents:**
- What is a 403 error?
- Why it works in browser but not script
- Detailed explanation of each diagnostic tool
- Step-by-step troubleshooting process
- Header explanations
- Additional tips (VPN, delays, cookies, etc.)

---

## Quick Start - Recommended Approach

### Option 1: Quick Fix (Easiest)
```bash
python3 scrape_fixed.py
```
If this works, you're done! Use this instead of scrape.py.

### Option 2: Diagnose First (Recommended)
```bash
python3 diagnose_403.py
```
See which header configurations work for your network.

### Option 3: Match Your Browser Exactly
```bash
python3 capture_headers.py
```
Then follow instructions to capture Samsung browser headers.

---

## Understanding the Fix

### Why Original Script May Fail
```python
# This is what an old script might send:
GET /location/hough-end-leisure-centre/fitness-classes-c HTTP/1.1
Host: bookings.better.org.uk
# ... minimal or no User-Agent
```

**Server might think:** "This doesn't have a User-Agent or proper headers. BLOCK IT!" → 403

### Why Updated Script Uses Scraper-Friendly User-Agent
```python
# This is what scrape.py and scrape_fixed.py now send:
GET /location/hough-end-leisure-centre/fitness-classes-c HTTP/1.1
Host: bookings.better.org.uk
User-Agent: mcr_fit_sniper/1.0 (+https://github.com/davegoopot/mcr_fit_sniper)
Accept: application/json
Accept-Language: en-GB,en;q=0.9
# ... more headers
```

**This approach:**
- Properly identifies the bot (transparent and ethical)
- Provides a way for website owners to learn about/contact the project
- Follows web scraping best practices (RFC 9309)
- Is more respectful than pretending to be a browser

---

## Files in This PR

| File | Purpose | Usage |
|------|---------|-------|
| `diagnose_403.py` | Test different headers | `python3 diagnose_403.py` |
| `capture_headers.py` | Capture browser headers | `python3 capture_headers.py` |
| `scrape_fixed.py` | Fixed scraping script | `python3 scrape_fixed.py` |
| `TROUBLESHOOTING_403.md` | Complete guide | Read for details |
| `README.md` | Updated documentation | Overview + quick start |
| `QUICKSTART.md` | This file | Quick reference |

---

## Next Steps

1. **Try scrape_fixed.py first:**
   ```bash
   python3 scrape_fixed.py
   ```

2. **If it still fails, run diagnostics:**
   ```bash
   python3 diagnose_403.py
   ```

3. **If diagnostics show all tests fail:**
   - Try from a different network
   - Use a VPN
   - Run capture_headers.py to get exact browser headers
   - Check TROUBLESHOOTING_403.md for more options

4. **If it works, update your original script:**
   - Copy the headers from scrape_fixed.py to scrape.py
   - Or just use scrape_fixed.py instead

---

## Support

If you're still having issues:
1. Read TROUBLESHOOTING_403.md thoroughly
2. Check the diagnostic script outputs
3. Try different networks/VPN
4. Verify the website works in your browser
5. Check if the site has a public API

---

## Summary

**Problem:** HTTP errors can occur due to missing or improper headers  
**Solution:** Use a scraper-friendly User-Agent that identifies the bot and references the repository  
**Approach:** Transparent and ethical web scraping following best practices  
**Tools Provided:** Diagnostic scripts + updated scripts + comprehensive docs  
**Time to Fix:** Immediate - scripts are already updated!  

✅ All scripts now use scraper-friendly User-Agent!

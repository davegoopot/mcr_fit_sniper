# 403 Error Diagnostic Tools - Quick Start Guide

## Problem
The `scrape.py` script returns a **403 Forbidden** error, but the same URL works fine in a Samsung Android browser.

## Root Cause
The script doesn't send proper browser headers. Websites use anti-bot protection that blocks requests without:
- User-Agent header (identifies the browser)
- Accept headers (content types)
- Other browser-specific headers

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
- Test 1: Basic request (no headers) - reproduces your 403 error
- Test 2: Minimal User-Agent
- Test 3: Chrome User-Agent
- Test 4: Samsung Android User-Agent (matches your working browser)
- Test 5: Full browser headers
- Test 6: With Referer header

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
- User-Agent: Chrome on Windows
- Accept headers for HTML/XML/images
- Accept-Language: English
- Accept-Encoding: gzip, deflate, br
- Security headers: Sec-Fetch-*
- Connection and cache control
- Better error messages with troubleshooting tips

**Key differences from original:**
```python
# Original scrape.py
response = requests.get(url, timeout=30)

# scrape_fixed.py
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Accept": "text/html,application/xhtml+xml,...",
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

### Why Original Script Fails
```python
# This is what scrape.py sends:
GET /location/hough-end-leisure-centre/fitness-classes-c HTTP/1.1
Host: bookings.better.org.uk
# ... minimal headers
```

**Server thinks:** "This doesn't look like a browser. It's probably a bot. BLOCK IT!" → 403

### Why Fixed Script Works
```python
# This is what scrape_fixed.py sends:
GET /location/hough-end-leisure-centre/fitness-classes-c HTTP/1.1
Host: bookings.better.org.uk
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...
Accept: text/html,application/xhtml+xml,application/xml;q=0.9...
Accept-Language: en-US,en;q=0.9
Accept-Encoding: gzip, deflate, br
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
# ... more headers
```

**Server thinks:** "This looks like Chrome browser. Okay, proceed!" → 200 OK

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

**Problem:** 403 Forbidden error due to missing browser headers  
**Solution:** Add proper User-Agent and browser headers  
**Tools Provided:** 3 diagnostic scripts + 1 fixed script + comprehensive docs  
**Time to Fix:** 1-2 minutes with scrape_fixed.py, or 5-10 minutes with diagnostics  

✅ All scripts are tested and ready to use!

# mcr_fit_sniper
Tools to help book fitness classes in the Manchester, UK area.

## Scripts

### scrape.py
Main scraping script that downloads fitness class information from the booking website and extracts active class dates.

The script uses a scraper-friendly User-Agent that properly identifies the bot and references this repository, following web scraping best practices.

```bash
python3 scrape.py
```

## Troubleshooting 403 Errors

If you're getting a **403 Forbidden** error when running scrape.py, we've provided diagnostic tools to help:

### Diagnostic Tools

1. **diagnose_403.py** - Automated testing of different header configurations
   ```bash
   python3 diagnose_403.py
   ```
   Tests multiple header combinations to identify what works.

2. **capture_headers.py** - Capture your browser's headers
   ```bash
   python3 capture_headers.py
   ```
   Then visit `http://localhost:8000` for instructions on capturing headers from your working browser.

3. **TROUBLESHOOTING_403.md** - Comprehensive troubleshooting guide
   
   Read this for detailed explanations and step-by-step instructions.

### Why 403 Errors Occur

403 errors happen when websites block requests that don't look legitimate. The script uses a scraper-friendly User-Agent (mcr_fit_sniper/1.0 +URL) that properly identifies the bot instead of pretending to be a browser, following web scraping best practices.

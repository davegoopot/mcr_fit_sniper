# mcr_fit_sniper
Tools to help book fitness classes in the Manchester, UK area.

## Scripts

### scrape.py
Main scraping script that downloads fitness class information from the booking website and extracts active class dates.

The script includes proper User-Agent headers to avoid 403 Forbidden errors.

```bash
python3 scrape.py
```

## Running on Termux (Android)

You can run this script automatically every 30 minutes on your Android device using Termux. This is useful for continuously monitoring new fitness class availability.

### Prerequisites

First, install the required packages in Termux:

```bash
# Update packages
pkg update && pkg upgrade

# Install Python and required tools
pkg install python git cronie termux-services

# Install Python dependencies
pip install requests
```

### Option 1: Using Cronie (Recommended)

Cronie provides traditional cron functionality in Termux.

1. **Start the cron service:**
   ```bash
   sv-enable crond
   ```

2. **Edit your crontab:**
   ```bash
   crontab -e
   ```

3. **Add the following line to run the script every 30 minutes:**
   ```bash
   */30 * * * * cd ~/mcr_fit_sniper && python3 scrape.py >> scrape.log 2>&1
   ```
   
   Note: Replace `~/mcr_fit_sniper` with the actual path to your cloned repository (e.g., `~/fitness-scraper` if you cloned it with a different name).

4. **Save and exit the editor** (in nano: Ctrl+X, then Y, then Enter)

5. **Verify the cron job is scheduled:**
   ```bash
   crontab -l
   ```

### Option 2: Using Termux:API Job Scheduler

If you prefer using Android's native job scheduler, you can use `termux-job-scheduler` (requires Termux:API app):

1. **Install Termux:API:**
   - Install the Termux:API app from F-Droid
   - Install the API package: `pkg install termux-api`

2. **Create a script to run the scraper:**
   ```bash
   nano ~/run-scraper.sh
   ```
   
   Add the following content:
   ```bash
   #!/data/data/com.termux/files/usr/bin/bash
   cd ~/mcr_fit_sniper
   python3 scrape.py >> scrape.log 2>&1
   ```
   
   Note: Replace `~/mcr_fit_sniper` with your actual repository path.

3. **Make the script executable:**
   ```bash
   chmod +x ~/run-scraper.sh
   ```

4. **Schedule the job to run every 30 minutes:**
   ```bash
   termux-job-scheduler --script ~/run-scraper.sh --period-ms 1800000
   ```
   
   Note: 1800000 milliseconds = 30 minutes

### Monitoring the Script

To view the output from automated runs (replace `~/mcr_fit_sniper` with your repository path):

```bash
# View the last 50 lines of the log
tail -n 50 ~/mcr_fit_sniper/scrape.log

# Watch the log in real-time
tail -f ~/mcr_fit_sniper/scrape.log
```

### Keeping Termux Running

For the scheduled tasks to work reliably:

1. **Acquire a wakelock** to prevent Termux from being killed:
   ```bash
   termux-wake-lock
   ```

2. **Disable battery optimization** for Termux in Android settings:
   - Go to Settings → Apps → Termux
   - Battery → Unrestricted

3. Consider using **Termux:Boot** to start services automatically on device boot.

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

403 errors happen when websites block requests that don't look like they're from a real browser. The original script uses minimal headers, which triggers anti-bot protection. The solution is to add proper browser headers (User-Agent, Accept, etc.) to make requests look legitimate.

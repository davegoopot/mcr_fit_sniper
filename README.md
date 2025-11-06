# mcr_fit_sniper
Tools to help book fitness classes in the Manchester, UK area.

## Scripts

### scrape.py
Main scraping script that downloads fitness class information from the booking website and extracts active class dates.

The script uses a scraper-friendly User-Agent that properly identifies the bot and references this repository, following web scraping best practices.

```bash
python3 scrape.py
# or with uv
uv run scrape.py
```

### list_schedule.py
Standalone utility script to list all registered termux-job-scheduler schedules.

```bash
python3 list_schedule.py
# or with uv
uv run list_schedule.py
```

This script will:
- Display all scheduled jobs configured with termux-job-scheduler
- Show job details including script path, period, and other settings
- Provide helpful commands for managing scheduled jobs
- Work both in Termux and non-Termux environments (with warnings)

## Running on Termux (Android)

You can run this script automatically every 30 minutes on your Android device using Termux. This is useful for continuously monitoring new fitness class availability.

### Using Termux:API Job Scheduler

You can use `termux-job-scheduler` to schedule the script to run every 30 minutes (requires Termux:API app):

#### Quick Setup (Recommended)

1. **Install Termux:API:**
   - Install the Termux:API app from F-Droid
   - Install the API package: `pkg install termux-api`

2. **Run the installation script:**
   ```bash
   ./install_scheduler.sh
   ```
   
   This script will automatically:
   - Update `run-scraper.sh` with the correct repository path
   - Make the script executable
   - Schedule the job to run every 30 minutes

#### Manual Setup

If you prefer to set up manually:

1. **Install Termux:API:**
   - Install the Termux:API app from F-Droid
   - Install the API package: `pkg install termux-api`

2. **Set up the scheduler script:**
   
   The repository includes `run-scraper.sh` which is pre-configured to run the scraper. If you cloned the repository to a different location, edit the script to update the paths:
   
   ```bash
   nano run-scraper.sh
   ```
   
   Update the paths in the script to match your repository location (replace `~/mcr_fit_sniper` with your actual path).

3. **Schedule the job to run every 30 minutes:**
   ```bash
   termux-job-scheduler --script ./run-scraper.sh --period-ms 1800000
   ```
   
   Note: 1800000 milliseconds = 30 minutes

### Managing Scheduled Jobs

#### List scheduled jobs
To view all registered scheduled jobs:

```bash
python3 list_schedule.py
# or with uv
uv run list_schedule.py
```

#### View logs
To view the output from automated runs (replace `~/mcr_fit_sniper` with your repository path):

```bash
# View the last 50 lines of the log
tail -n 50 ~/mcr_fit_sniper/scrape.log

# Watch the log in real-time
tail -f ~/mcr_fit_sniper/scrape.log
```

#### Cancel scheduled jobs
To cancel all scheduled jobs:

```bash
termux-job-scheduler --cancel-all
```

### Keeping Termux Running

The `termux-job-scheduler` uses Android's JobScheduler API, which handles scheduling reliably in the background. However:

1. **Disable battery optimization** for both Termux and Termux:API in Android settings:
   - Go to Settings → Apps → Termux → Battery → Unrestricted
   - Go to Settings → Apps → Termux:API → Battery → Unrestricted
   
   This ensures the Termux:API app can execute scheduled jobs even when the device is in power-saving mode.

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

#!/data/data/com.termux/files/usr/bin/bash
# Installation script to set up termux-job-scheduler for the fitness class scraper
# This script automatically configures the paths and schedules the job

set -e  # Exit on error

echo "================================================"
echo "Termux Job Scheduler Installation Script"
echo "================================================"
echo ""

# Get the absolute path of the repository (where this script is located)
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Repository directory: $REPO_DIR"
echo ""

# Check if termux-api is installed
if ! command -v termux-job-scheduler &> /dev/null; then
    echo "ERROR: termux-job-scheduler not found!"
    echo "Please install Termux:API first:"
    echo "  1. Install Termux:API app from F-Droid"
    echo "  2. Run: pkg install termux-api"
    exit 1
fi

# Update run-scraper.sh with the current directory path
echo "Updating run-scraper.sh with current directory path..."
sed -i "s|cd ~/mcr_fit_sniper|cd $REPO_DIR|g" "$REPO_DIR/run-scraper.sh"
sed -i "s|>> ~/mcr_fit_sniper/scrape.log|>> $REPO_DIR/scrape.log|g" "$REPO_DIR/run-scraper.sh"
echo "✓ Updated run-scraper.sh"
echo ""

# Make sure the script is executable
chmod +x "$REPO_DIR/run-scraper.sh"
echo "✓ Made run-scraper.sh executable"
echo ""

# Schedule the job with termux-job-scheduler
echo "Scheduling job to run every 30 minutes..."
termux-job-scheduler --script "$REPO_DIR/run-scraper.sh" --period-ms 1800000

if [ $? -eq 0 ]; then
    echo "✓ Job scheduled successfully!"
    echo ""
    echo "================================================"
    echo "Installation Complete!"
    echo "================================================"
    echo ""
    echo "The scraper will now run automatically every 30 minutes."
    echo ""
    echo "To view logs:"
    echo "  tail -f $REPO_DIR/scrape.log"
    echo ""
    echo "To check scheduled jobs:"
    echo "  termux-job-scheduler --show"
    echo ""
    echo "To cancel the scheduled job:"
    echo "  termux-job-scheduler --cancel-all"
    echo ""
else
    echo "ERROR: Failed to schedule job"
    exit 1
fi

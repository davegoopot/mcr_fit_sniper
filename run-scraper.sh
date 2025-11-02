#!/data/data/com.termux/files/usr/bin/bash
# Script to run the fitness class scraper with uv
# This script is designed to be scheduled with termux-job-scheduler

# Change to the repository directory
# Note: Update this path to match your actual repository location
cd ~/mcr_fit_sniper

# Run the scraper script using uv and log the output
uv run scrape.py >> ~/mcr_fit_sniper/scrape.log 2>&1

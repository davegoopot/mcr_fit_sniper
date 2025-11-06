#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

"""
Standalone script to list registered termux-job-scheduler schedules.
This script displays all scheduled jobs configured with termux-job-scheduler.
"""

import subprocess
import sys
import os
import json
from datetime import datetime
from typing import Optional


def is_termux() -> bool:
    """
    Check if the script is running in Termux environment.
    
    Returns:
        bool: True if running in Termux, False otherwise
    """
    # Check for TERMUX_VERSION environment variable
    return bool(os.environ.get("TERMUX_VERSION"))


def check_termux_api_installed() -> bool:
    """
    Check if termux-api package is installed.
    
    Returns:
        bool: True if termux-job-scheduler command is available, False otherwise
    """
    try:
        result = subprocess.run(
            ["which", "termux-job-scheduler"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def get_scheduled_jobs() -> Optional[str]:
    """
    Retrieve scheduled jobs from termux-job-scheduler.
    
    Returns:
        Optional[str]: Output from termux-job-scheduler --show command, or None if failed
    """
    try:
        result = subprocess.run(
            ["termux-job-scheduler", "--show"],
            capture_output=True,
            text=True,
            timeout=10,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running termux-job-scheduler: {e}", file=sys.stderr)
        if e.stderr:
            print(f"Error details: {e.stderr}", file=sys.stderr)
        return None
    except subprocess.TimeoutExpired:
        print("Error: termux-job-scheduler command timed out", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("Error: termux-job-scheduler command not found", file=sys.stderr)
        return None


def parse_and_display_jobs(output: str) -> None:
    """
    Parse and display scheduled jobs in a readable format.
    
    Args:
        output: Raw output from termux-job-scheduler --show
    """
    if not output or output.lower() == "no scheduled jobs":
        print("\n📋 No scheduled jobs found.")
        print("\nTo schedule the scraper, run:")
        print("  ./install_scheduler.sh")
        print("\nOr manually:")
        print("  termux-job-scheduler --script ./run-scraper.sh --period-ms 1800000")
        return
    
    print("\n" + "="*60)
    print("📅 Registered Termux Job Scheduler Jobs")
    print("="*60)
    
    # Try to parse the output
    # termux-job-scheduler --show output format can vary
    lines = output.split('\n')
    
    job_count = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if line contains job information
        if "job id" in line.lower() or "script" in line.lower() or "period" in line.lower():
            job_count += 1
            print(f"\n{line}")
        elif line:
            print(f"  {line}")
    
    # If no structured output found, just display raw output
    if job_count == 0 and output:
        print(f"\n{output}")
    
    print("\n" + "="*60)
    
    # Display helpful information
    print("\n💡 Useful Commands:")
    print("  • View logs:        tail -f ~/mcr_fit_sniper/scrape.log")
    print("  • Cancel all jobs:  termux-job-scheduler --cancel-all")
    print("  • Reschedule:       ./install_scheduler.sh")
    print()


def main() -> int:
    """
    Main function to list termux-job-scheduler schedules.
    
    Returns:
        int: Exit code (0 for success, non-zero for error)
    """
    print("Termux Job Scheduler - List Registered Schedules")
    print("-" * 60)
    
    # Check if running in Termux
    if not is_termux():
        print("\n⚠️  Warning: Not running in Termux environment")
        print("This script is designed for Termux on Android.")
        print("The TERMUX_VERSION environment variable was not found.")
        print("\nContinuing anyway...\n")
    
    # Check if termux-api is installed
    if not check_termux_api_installed():
        print("\n❌ Error: termux-job-scheduler not found!")
        print("\nPlease install Termux:API:")
        print("  1. Install Termux:API app from F-Droid")
        print("  2. Run: pkg install termux-api")
        print("  3. Grant necessary permissions to Termux:API app")
        print()
        return 1
    
    # Get scheduled jobs
    output = get_scheduled_jobs()
    
    if output is None:
        print("\n❌ Failed to retrieve scheduled jobs")
        print("Please ensure:")
        print("  • Termux:API app is installed")
        print("  • termux-api package is installed (pkg install termux-api)")
        print("  • Necessary permissions are granted to Termux:API")
        print()
        return 1
    
    # Parse and display jobs
    parse_and_display_jobs(output)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

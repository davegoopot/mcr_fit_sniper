#!/usr/bin/env python3
"""
Unregister all Termux scheduled tasks for the fitness class scraper.
This script removes all jobs scheduled with termux-job-scheduler.
"""

import subprocess
import sys
import shutil


def print_header():
    """Print the script header."""
    print("=" * 48)
    print("Termux Job Scheduler Uninstall Script")
    print("=" * 48)
    print()


def check_termux_scheduler():
    """Check if termux-job-scheduler command is available."""
    if not shutil.which("termux-job-scheduler"):
        print("ERROR: termux-job-scheduler not found!")
        print("Please install Termux:API first:")
        print("  1. Install Termux:API app from F-Droid")
        print("  2. Run: pkg install termux-api")
        return False
    return True


def show_scheduled_jobs():
    """Display currently scheduled jobs."""
    print("Checking currently scheduled jobs...")
    try:
        result = subprocess.run(
            ["termux-job-scheduler", "--show"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.stdout.strip():
            print("Current scheduled jobs:")
            print(result.stdout)
        else:
            print("No jobs currently scheduled.")
            
    except subprocess.CalledProcessError as e:
        print(f"Warning: Could not retrieve scheduled jobs: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")


def cancel_all_jobs():
    """Cancel all scheduled jobs."""
    print("Canceling all scheduled jobs...")
    try:
        result = subprocess.run(
            ["termux-job-scheduler", "--cancel-all"],
            capture_output=True,
            text=True,
            check=True
        )
        
        print("✓ All scheduled jobs have been canceled!")
        if result.stdout.strip():
            print(result.stdout)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to cancel scheduled jobs: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False


def print_footer():
    """Print the script footer with helpful information."""
    print()
    print("=" * 48)
    print("Uninstall Complete!")
    print("=" * 48)
    print()
    print("All scheduled jobs have been removed.")
    print()
    print("To schedule jobs again:")
    print("  ./install_scheduler.sh")
    print()
    print("To check scheduled jobs:")
    print("  termux-job-scheduler --show")
    print()


def main():
    """Main function to unregister all Termux scheduled tasks."""
    print_header()
    
    # Check if termux-job-scheduler is available
    if not check_termux_scheduler():
        sys.exit(1)
    
    print()
    
    # Show current scheduled jobs
    show_scheduled_jobs()
    
    print()
    
    # Cancel all jobs
    if cancel_all_jobs():
        print_footer()
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

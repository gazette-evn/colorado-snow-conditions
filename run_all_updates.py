#!/usr/bin/env python3
"""
Master Update Script for Colorado Snow Conditions
Runs all update pipelines and logs results
"""

import subprocess
import sys
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("master_update.log"),
        logging.StreamHandler()
    ]
)

def run_script(script_name, description):
    """
    Run a Python script and return success status
    
    Args:
        script_name: Name of Python script to run
        description: Human-readable description for logging
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logging.info(f"Starting {description}...")
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout per script
        )
        
        if result.returncode == 0:
            logging.info(f"✅ {description} completed successfully")
            return True
        else:
            logging.error(f"❌ {description} failed")
            logging.error(f"Error output:\n{result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logging.error(f"❌ {description} timed out (>5 minutes)")
        return False
    except Exception as e:
        logging.error(f"❌ {description} failed with exception: {e}")
        return False


def main():
    """Main orchestration function"""
    start_time = datetime.now()
    
    logging.info("🎿" * 30)
    logging.info("COLORADO SNOW CONDITIONS - UPDATE PIPELINE")
    logging.info("🎿" * 30)
    logging.info(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define all update scripts
    # Order: Scrape data → Update Google Sheets → Datawrapper reads from Sheets
    scripts = [
        ("combined_scraper.py", "Combined Resort Data Scraper"),
        ("google_sheets_updater.py", "Google Sheets Update"),
    ]
    
    # Run each script and track results
    results = {}
    for script, description in scripts:
        results[description] = run_script(script, description)
    
    # Calculate summary
    end_time = datetime.now()
    duration = end_time - start_time
    successful = sum(results.values())
    total = len(results)
    
    # Print summary
    logging.info("\n" + "=" * 70)
    logging.info("UPDATE SUMMARY")
    logging.info("=" * 70)
    
    for description, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        logging.info(f"{description}: {status}")
    
    logging.info("-" * 70)
    logging.info(f"Completed: {successful}/{total} updates successful")
    logging.info(f"Duration: {duration}")
    logging.info(f"Finished at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info("=" * 70)
    
    # Return exit code (0 = success, 1 = failure)
    return 0 if successful == total else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)


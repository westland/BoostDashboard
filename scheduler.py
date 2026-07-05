import schedule
import time
from datetime import datetime
import os
import sys

# Ensure project root is in sys.path to allow imports
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from src.wow_boosting_leads.main import run
except ImportError:
    from src.wow_boosting_leads.main import run

def job():
    print(f"[{datetime.now().isoformat()}] Starting scheduled lead generation job...")
    try:
        run()
    except Exception as e:
        print(f"[{datetime.now().isoformat()}] Scheduler job encountered error: {e}")

# Schedule task to run daily at 9:00 AM
schedule.every().day.at("09:00").do(job)

print("⏰ WoW Leads Scheduler is active. Press Ctrl+C to terminate.")
print("The job is scheduled to run every day at 09:00.")

# Run the job immediately once on startup for easy debugging/testing
job()

while True:
    try:
        schedule.run_pending()
        time.sleep(10)
    except KeyboardInterrupt:
        print("\nStopping scheduler...")
        break

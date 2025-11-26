import schedule
import time
from spotify_client import get_recently_played
from db_functions import save_history_entries

def job():
    print("Running scheduled job...")
    history = get_recently_played()
    save_history_entries(history)
    print("History synced 🔁.")

def start_scheduler():
    # schedule.every(10).minutes.do(job)
    schedule.every(10).seconds.do(job)

    print("Scheduler started. Running every 10 minutes...")

    while True:
        schedule.run_pending()
        time.sleep(1)

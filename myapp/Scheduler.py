
from apscheduler.schedulers.background import BackgroundScheduler
from .utils import fetch_and_update_crypto_data

def StartScheduler(ApiKey):
    scheduler = BackgroundScheduler()
    # Scheduled the function to run every 5 minutes
    scheduler.add_job(fetch_and_update_crypto_data, 'interval', minutes=5, args=[ApiKey])
    scheduler.start()

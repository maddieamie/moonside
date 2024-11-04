from huey import crontab
from .utils import fetch_moon_phase_data

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')


@huey.periodic_task(crontab(hour='0'))  # Runs at midnight
def scheduled_moon_phase_fetch(api_key):
    
    fetch_moon_phase_data(api_key)

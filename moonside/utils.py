# myapp/tasks.py or myapp/utils.py
import requests
from datetime import datetime, timedelta
from .models import MoonPhase

def fetch_moon_phase_data(api_key, location="Seattle", days=10):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days={days}&aqi=no&alerts=no"
    response = requests.get(url)
    if response.status_code == 200:
        forecast_days = response.json()["forecast"]["forecastday"]
        for day_data in forecast_days:
            date_str = day_data["date"]
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            moon_data = day_data["astro"]
            MoonPhase.objects.update_or_create(
                date=date_obj,
                defaults={
                    "phase": moon_data["moon_phase"],
                    "moonrise": moon_data["moonrise"],
                    "moonset": moon_data["moonset"],
                    "sunrise": moon_data["sunrise"],
                    "sunset": moon_data["sunset"],
                    "illumination": int(moon_data["moon_illumination"]),
                }
            )



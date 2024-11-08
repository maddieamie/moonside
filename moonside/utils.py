# myapp/tasks.py or myapp/utils.py
import requests
from datetime import datetime, timedelta
from .models import MoonPhase
from django.templatetags.static import static
import uuid

def fetch_moon_phase_data(api_key, location="Seattle", days=3):
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
                    "uuid": uuid.uuid4()
                }
            )



def get_moon_phase_image(phase):
    # Map moon phases to specific image filenames
    phase_image_map = {
        "New Moon": "moon_images/new_moon.png",
        "First Quarter": "moon_images/first_quarter.png",
        "Full Moon": "moon_images/full_moon.png",
        "Last Quarter": "moon_images/last_quarter.png",
        "Waxing Crescent": "moon_images/waxing_crescent.png",
        "Waxing Gibbous": "moon_images/waxing_gibbous.png",
        "Waning Crescent": "moon_images/waning_crescent.png",
        "Waning Gibbous": "moon_images/waning_gibbous.png",
    }
    # Return the corresponding image path or a default image if not found
    image_path = phase_image_map.get(phase, "moon_images/default.png")
    return static(image_path)



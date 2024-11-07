from huey import crontab
from moonside.models import MoonPhase
from moonside.utils import fetch_moon_phase_data

@huey.periodic_task(crontab(hour=0, minute=0))  # Runs daily at midnight
def update_moon_data():
    for phase in MoonPhase.objects.all():
        fetch_moon_phase_data(phase)


from django.shortcuts import render
from django.views.decorators.cache import cache_page
from datetime import date, timedelta
from moony.settings.base import SITE_VERSION
from .models import MoonPhase, CustomUser


def moon_phase_calendar_view(request):
    today = date.today()
    days_range = [today + timedelta(days=i) for i in range(10)]
    moon_data = MoonPhase.objects.filter(date__in=days_range).order_by("date")
    return render(request, "moon_calendar.html", {"moon_data": moon_data})


# 30 days cache, example using site version to invalidate cache (increment to
# invalidate)
@cache_page(60 * 60 * 24 * 30,
            key_prefix=SITE_VERSION)
def home(request):
    return render(request, 'moonside/home.html')

from django.shortcuts import render
from django.views.decorators.cache import cache_page
from datetime import date, timedelta
from moony.settings.base import SITE_VERSION
from .models import MoonPhase, UserJournalEntry
from django.utils import timezone
from .utils import get_moon_phase_image

from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .permissions import IsOwnerOrReadOnly
from .serializers import JournalSerializer

import requests
from django.http import JsonResponse
from django.conf import settings

def get_moon_phase(request):
    # External API URL and parameters
    api_url = "https://api.weatherapi.com/v1/astronomy.json"
    params = {
        "key": API_KEY,  # Your API key from .env or settings
        "q": "Seattle",
        "dt": "2024-11-05"  # Example date for the data you want
    }
    
    # Make a GET request to the external API
    response = requests.get(api_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        return JsonResponse(data)  # Send data as JSON to your frontend
    else:
        return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get today's date
        today = timezone.now().date()
        
        # Fetch today's moon phase data
        moon_phase = MoonPhase.objects.filter(date=today).first()
        if moon_phase:
            # Use the get_moon_phase_image function to get the image URL
            context['moon_phase'] = moon_phase
            context['moon_image'] = get_moon_phase_image(moon_phase.phase)
        else:
            context['moon_phase'] = None 

        # If user is authenticated, check if they have an entry for today
        if self.request.user.is_authenticated:
            user_entry = UserJournalEntry.objects.filter(
                user=self.request.user,
                moon_phase=moon_phase  # Link entry to today's moon phase
            ).first()
            context['user_entry'] = user_entry

        return context


class CalendarView(TemplateView):
    template_name = "moon_calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Step 1: Get today's date and the range for the current month
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month.replace(month=(today.month % 12) + 1) - timedelta(days=1))
        
        # Step 2: Fetch moon phase data for the current month from the database
        moon_data = MoonPhase.objects.filter(date__range=(start_of_month, end_of_month)).order_by("date")
        context['moon_data'] = moon_data

        # Step 3: Get the user’s location if available, otherwise use "Seattle"
        user = self.request.user
        location = getattr(user, "location", "Seattle") if user.is_authenticated else "Seattle"
        
        # Step 4: Fetch a 3-day weather forecast using the user’s location
        weather_api_url = "https://api.weatherapi.com/v1/forecast.json"
        params = {
            "key": settings.API_KEY,
            "q": location,
            "days": 3
        }

        try:
            response = requests.get(weather_api_url, params=params)
            response.raise_for_status()  # Check for HTTP errors
            forecast_data = response.json().get("forecast", {}).get("forecastday", [])
            forecast_with_images = [
                {
                    "date": forecast_day["date"],
                    "phase": forecast_day["astro"]["moon_phase"],  
                    "illumination": forecast_day["astro"]["moon_illumination"],
                    "moonrise": forecast_day["astro"]["moonrise"],
                    "moonset": forecast_day["astro"]["moonset"],
                    "image": get_moon_phase_image(forecast_day["astro"]["moon_phase"]),  
                }
                for forecast_day in forecast_data
            ]
            context['three_day_forecast'] = forecast_with_images
            context['location'] = location  # Save the actual location used

        except requests.RequestException:
            # Fallback to Seattle if the API request fails
            params['q'] = "Seattle"
            fallback_response = requests.get(weather_api_url, params=params)
            fallback_response.raise_for_status()
            fallback_forecast = fallback_response.json().get("forecast", {}).get("forecastday", [])
            fallback_with_images = [
                {
                    "date": fallback_day["date"],
                    "phase": fallback_day["astro"]["moon_phase"],
                    "illumination": fallback_day["astro"]["moon_illumination"],
                    "moonrise": fallback_day["astro"]["moonrise"],
                    "moonset": fallback_day["astro"]["moonset"],
                    "image": get_moon_phase_image(fallback_day["astro"]["moon_phase"]),
                }
                for fallback_day in fallback_forecast
            ]
            context['three_day_forecast'] = fallback_with_images
            context['location'] = "Seattle"

        # Step 5: Add a note about Seattle-specific moon phase data
        context['location_note'] = "Currently, moon phase data is available only for Seattle."

        return context


class UserJournalEntryList(LoginRequiredMixin, ListView):
    template_name = "journal_entries.html"
    model = UserJournalEntry
    context_object_name = "entries"

class UserJournalEntryDetailView(LoginRequiredMixin, DetailView):
    template_name = "journal_entry_detail.html"
    model = UserJournalEntry

class UserJournalEntryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "update_entry.html"
    model = UserJournalEntry
    fields = "__all__"

class UserJournalEntryCreateView(LoginRequiredMixin, CreateView):
    template_name = "create_entry.html"
    model = UserJournalEntry
    fields = "__all__"
    success_url = reverse_lazy("journal_entries")

class UserJournalEntryDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "delete_entry.html"
    model = UserJournalEntry
    success_url = reverse_lazy("journal_entries")
    

class UserJournalEntryListA(ListCreateAPIView):
    queryset = UserJournalEntry.objects.all()
    serializer_class = JournalSerializer


class UserJournalEntryDetailA(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = UserJournalEntry.objects.all()
    serializer_class = JournalSerializer

# 30 days cache, example using site version to invalidate cache (increment to
# invalidate)
@cache_page(60 * 60 * 24 * 30,
            key_prefix=SITE_VERSION)
def home(request):
    return render(request, 'moonside/home.html')

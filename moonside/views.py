from django.shortcuts import render
from django.views.decorators.cache import cache_page
from datetime import date, timedelta
from moony.settings.base import SITE_VERSION
from .models import MoonPhase, UserJournalEntry

from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .permissions import IsOwnerOrReadOnly
from .serializers import JournalSerializer

class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["moon_phase"] = MoonPhase.objects.filter(date=date.today()).first()
        return context

class CalendarView(TemplateView):
    template_name ="moon_calendar.html"

    def moon_phase_calendar_view(request):
        today = date.today()
        days_range = [today + timedelta(days=i) for i in range(10)]
        moon_data = MoonPhase.objects.filter(date__in=days_range).order_by("date")
        return render(request, "moon_calendar.html", {"moon_data": moon_data})

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

class UserJournalEntryDeleteView(LoginRequiredMixin, DeleteView):
    tmeplate_name = "delete_entry.html"
    model = UserJournalEntry
    success_url = reverse_lazy("journal_entries.html")
    


# 30 days cache, example using site version to invalidate cache (increment to
# invalidate)
@cache_page(60 * 60 * 24 * 30,
            key_prefix=SITE_VERSION)
def home(request):
    return render(request, 'moonside/home.html')

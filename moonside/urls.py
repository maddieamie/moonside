from django.urls import path

from .views import (
    CalendarView,
    UserJournalEntryCreateView,
    UserJournalEntryDeleteView,
    UserJournalEntryDetailView,
    UserJournalEntryList,
    UserJournalEntryUpdateView,
    HomePageView,
)

# after login, go to homepage. put calendar on nav.

urlpatterns = [
    path('', HomePageView.as_view(), name='moonside'),
    path("calendar/", CalendarView.as_view(), name="moon_calendar"),
    path("journal-entries/", UserJournalEntryList.as_view(), name="journal_entries"),
    path("<uuid:uuid_id>/", UserJournalEntryDetailView.as_view(), name="journal_entry_detail"),
    path("create/<uuid:moon_phase_uuid>/", UserJournalEntryCreateView.as_view(), name="create_entry"),
    path("<uuid:uuid_id>/update/", UserJournalEntryUpdateView.as_view(), name="update_entry"),
    path("<uuid:uuid_id>/delete/", UserJournalEntryDeleteView.as_view(), name="delete_entry"),
]
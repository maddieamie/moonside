# Register your models here.
from django.contrib import admin
from .models import MoonPhase, UserJournalEntry

# Register your models here.
admin.site.register(MoonPhase)
admin.site.register(UserJournalEntry)
# Create your models here.
from django.db import models
from accounts.models import CustomUser
from django.urls import reverse

class MoonPhase(models.Model):
    date = models.DateField(unique=True)
    phase = models.CharField(max_length=100)
    moonrise = models.TimeField(null=True, blank=True)
    moonset = models.TimeField(null=True, blank=True)
    sunrise = models.TimeField(null=True, blank=True)
    sunset = models.TimeField(null=True, blank=True)
    illumination = models.IntegerField()

    def __str__(self):
        return f"{self.date} - {self.phase}"

class UserJournalEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    moon_phase = models.ForeignKey(MoonPhase, on_delete=models.SET_NULL, null=True)
    ritual_text = models.TextField()
    intent_text = models.TextField()
    reflect_text = models.TextField()
    manifest_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Entry by {self.user.username} on {self.created_at}"
    
    def get_absolute_url(self):
        return reverse('journal_entry_detail', args=[str(self.id)])

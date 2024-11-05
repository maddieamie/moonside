from rest_framework import serializers
from .models import UserJournalEntry


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserJournalEntry
        fields = "__all__"

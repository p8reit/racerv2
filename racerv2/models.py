from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class TrackedRequest(models.Model):
    unique_id = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=45)
    user_agent = models.TextField(null=True, blank=True)
    referrer = models.TextField(null=True, blank=True)
    geolocation = models.TextField(null=True, blank=True)
    headers = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(
        'racerv2.Group',
        on_delete=models.CASCADE,
        null=True,  # Allow nulls for existing rows during migration
    )





class ConnectionRecord(models.Model):
    tracked_request = models.ForeignKey(
        TrackedRequest, 
        related_name="connections", 
        on_delete=models.CASCADE
    )
    ip_address = models.CharField(max_length=45)
    user_agent = models.TextField(null=True, blank=True)
    referrer = models.TextField(null=True, blank=True)
    headers = models.TextField(null=True, blank=True)
    is_google_hosted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

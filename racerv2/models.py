from django.db import models
from django.utils.timezone import now


class TrackedRequest(models.Model):
    unique_id = models.CharField(max_length=255, unique=True)
    ip_address = models.CharField(max_length=45)
    user_agent = models.TextField(null=True, blank=True)
    referrer = models.TextField(null=True, blank=True)
    geolocation = models.TextField(null=True, blank=True)
    headers = models.TextField(null=True, blank=True)
    group_name = models.CharField(max_length=255, null=True, blank=True)  # Optional group identifier
    is_hidden = models.BooleanField(default=True)  # Boolean to mark hidden requests
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request {self.unique_id} from {self.ip_address}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Tracked Request"
        verbose_name_plural = "Tracked Requests"


class ConnectionRecord(models.Model):
    tracked_request = models.ForeignKey(
        'TrackedRequest',
        on_delete=models.CASCADE,
        related_name='connection_records'
    )
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    referrer = models.URLField(blank=True, null=True)
    headers = models.JSONField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Connection to {self.tracked_request.unique_id} at {self.timestamp}"

    def __str__(self):
        return f"Connection from {self.ip_address}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Connection Record"
        verbose_name_plural = "Connection Records"
        
        



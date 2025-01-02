from django.db import models


class TrackedRequest(models.Model):
    unique_id = models.CharField(max_length=255, unique=True)
    ip_address = models.CharField(max_length=45)
    user_agent = models.TextField(null=True, blank=True)
    referrer = models.TextField(null=True, blank=True)
    geolocation = models.TextField(null=True, blank=True)
    headers = models.TextField(null=True, blank=True)
    group_name = models.CharField(max_length=255, null=True, blank=True)  # Optional group identifier
    is_hidden = models.BooleanField(default=False)  # Boolean to mark hidden requests
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request {self.unique_id} from {self.ip_address}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Tracked Request"
        verbose_name_plural = "Tracked Requests"


class ConnectionRecord(models.Model):
    tracked_request_id = models.CharField(max_length=255)  # Reference unique_id directly
    ip_address = models.CharField(max_length=45)
    user_agent = models.TextField(null=True, blank=True)
    referrer = models.TextField(null=True, blank=True)
    headers = models.TextField(null=True, blank=True)
    is_google_hosted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Connection from {self.ip_address}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Connection Record"
        verbose_name_plural = "Connection Records"

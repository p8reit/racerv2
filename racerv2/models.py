from django.db import models
from django.utils import timezone  # Import added here
from django.utils.timezone import now 

class TrackedRequest(models.Model):
    unique_id = models.CharField(max_length=255, unique=True)
    ip_address = models.CharField(max_length=64, blank=True, null=True)
    user_agent = models.TextField(null=True, blank=True)
    referrer = models.TextField(null=True, blank=True)
    geolocation = models.TextField(null=True, blank=True)
    headers = models.TextField(null=True, blank=True)
    group_name = models.CharField(max_length=255, null=True, blank=True)  # Optional group identifier
    is_hidden = models.BooleanField(default=False)  # Boolean to mark hidden requests
    timestamp = models.DateTimeField(auto_now_add=True)
    relay_count = models.IntegerField(default=0)  # Changed to IntegerField
    heat_score = models.FloatField(default=0.0)  # Heat score for relay detection

    def calculate_heat_score(self):
        """
        Calculate the heat score based on relay count and recent activity.
        """
        # Base score based on relay count
        base_score = self.relay_count

        # Increase score for high activity within the last 10 minutes
        recent_time = timezone.now() - timezone.timedelta(minutes=10)
        recent_connections = self.connection_records.filter(timestamp__gte=recent_time).count()

        # Calculate activity boost
        activity_boost = recent_connections * 1.5

        # Final heat score calculation
        self.heat_score = base_score + activity_boost
        self.save()

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
    ip_address = models.CharField(max_length=64, blank=True, null=True)
    user_agent = models.TextField()
    referrer = models.URLField(blank=True, null=True)
    headers = models.JSONField()
    timestamp = models.DateTimeField(default=now)
    is_google_hosted = models.BooleanField(default=True)

    def __str__(self):
        return f"Connection from {self.ip_address}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Connection Record"
        verbose_name_plural = "Connection Records"

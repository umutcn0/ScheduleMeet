from django.db import models

class Meet(models.Model):
    date = models.DateTimeField(blank=True, null=True)
    start_hour = models.TimeField(blank=True, null=True)
    end_hour = models.TimeField(blank=True, null=True)
    description = models.TextField()
    participants = models.TextField()
    is_deleted = models.BooleanField(default=False)

from django.db import models
from django.utils import timezone
import json


class LogMessage(models.Model):
    message = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"


class PredictionHistory(models.Model):
    bathrooms = models.FloatField()
    isparking = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    rooms = models.FloatField()
    size = models.FloatField()
    year = models.IntegerField()
    quarter = models.IntegerField()
    prediction_value = models.FloatField()
    log_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Prediction on {self.log_date} - Predicted Price: {self.prediction_value}"
        )

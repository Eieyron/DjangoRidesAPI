from django.db import models
from Ride.models import Ride

# Create your models here.
class RideEvent(models.Model):

    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    description = models.CharField(max_length = 150)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "RideEvent"
        verbose_name_plural = "RideEvents"

    def __str__(self):
        return f"{self.id_ride.id_ride}: {self.description}"


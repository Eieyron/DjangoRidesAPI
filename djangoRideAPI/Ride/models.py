from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

class Ride(models.Model):

    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ('en-route', 'En-route'),
            ('pickup', 'Pickup'),
            ('dropoff', 'Dropoff')
        ],
        default='en-route'
    )
    id_rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ride_rider')
    id_driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ride_driver')
    pickup_latitude = models.FloatField(null=True, blank=True)
    pickup_longitude = models.FloatField(null=True, blank=True)
    dropoff_latitude = models.FloatField(null=True, blank=True)
    dropoff_longitude = models.FloatField(null=True, blank=True)
    pickup_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return f"{self.id_ride}: {self.id_rider} | {self.id_driver}"

    class Meta:
        verbose_name = "Ride"
        verbose_name_plural = "Rides"

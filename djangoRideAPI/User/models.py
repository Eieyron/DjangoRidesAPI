from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    id_ride = models.AutoField(primary_key=True)
    role = models.CharField(
        max_length=10,
        choices=[
            ('admin', 'Admin'),
            ('rider', 'Rider'),
            ('driver', 'Driver')
        ],
        default='rider'
    )
    first_name = models.CharField(max_length = 150)
    last_name = models.CharField(max_length = 150)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length = 150)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    class Meta:
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'
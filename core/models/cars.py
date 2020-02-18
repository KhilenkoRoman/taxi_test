from django.db import models


class Car(models.Model):
    model = models.CharField(verbose_name='model', max_length=32)
    car_number = models.CharField(verbose_name='car number', max_length=16)
    is_available = models.BooleanField(default=True)

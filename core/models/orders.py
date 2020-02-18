from django.db import models
from core.models.cars import Car

ORDER_STATUS = (
    ('active', 'active'),
    ('inactive', 'inactive'),
)


class Order(models.Model):
    name = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=16)
    status = models.CharField(max_length=8, choices=ORDER_STATUS)
    order_address = models.TextField()
    target_address = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, related_name='order', null=True)
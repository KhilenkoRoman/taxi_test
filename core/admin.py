from django.contrib import admin
from core.models.cars import Car
from core.models.orders import Order


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'car_number', 'is_available')
    fields = ('model', 'car_number', 'is_available')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created', )
    list_display = ('id', 'name', 'phone_number', 'status')
    fields = ('name', 'phone_number', 'status', 'order_address', 'target_address', 'date_created', 'car')

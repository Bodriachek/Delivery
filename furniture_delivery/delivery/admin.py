from django.contrib import admin
from delivery.models import Order, RegistrationRefueling, Driver, Car, Manager


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Замовлення"""
    list_display = ('id', 'status', 'date_trip', 'product', 'name', 'phone', 'manager', 'driver', 'car')
    list_display_links = ('id', 'status', 'product')


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    """Замовлення"""
    list_display = ('id', 'user', 'categories')
    list_display_links = ('id', 'user')


# admin.site.register(Customer)
admin.site.register(RegistrationRefueling)
admin.site.register(Car)
admin.site.register(Manager)

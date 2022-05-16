from django.contrib import admin
from delivery.models import Order, Fueling, Driver, Car, Manager, Repair


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Замовлення"""
    list_display = ('id', 'status', 'date_trip', 'product', 'name', 'phone', 'manager', 'driver', 'car')
    list_display_links = ('id', 'status', 'product')


admin.site.register(Repair)
admin.site.register(Driver)
admin.site.register(Fueling)
admin.site.register(Car)
admin.site.register(Manager)

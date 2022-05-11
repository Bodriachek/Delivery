from django.db.models.signals import post_save
from django.dispatch import receiver
from delivery.models import Order, Driver


@receiver(post_save, sender=Driver)
def add_mileage(**kwargs):
    if Order.status == 'Завершено':
        Driver.mileage += Order.total_distance
        Driver.mileage.save()

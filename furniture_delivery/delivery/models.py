from datetime import date

from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Q
from multiselectfield import MultiSelectField


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Ім'я та прізвище", null=True)

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджери'



class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Ім'я та прізвище", null=True)
    CATEGORIES = (
        (1, 'B'),
        (2, 'C1'),
        (3, 'C'),
    )
    categories = MultiSelectField(choices=CATEGORIES, null=True, verbose_name='Категорії водія')

    @property
    def get_mileage(self):
        orders = self.orders.filter()
        r = 0
        for order in orders:
            r += order.total_distance
        return r

    class Meta:
        verbose_name = 'Водій'
        verbose_name_plural = 'Водії'


class Cars(models.Model):
    title = models.CharField(verbose_name='Назва', max_length=150, blank=True, null=True)
    state_number = models.CharField(verbose_name='Державний номер',
                                    max_length=10, null=True,
                                    help_text='Код регіону__регістраційний номер__серія')
    category = models.IntegerField(choices=Driver.CATEGORIES, verbose_name='Водійська категорія')
    responsible_driver = models.ForeignKey(Driver, on_delete=models.CASCADE,
                                           null=True, verbose_name='Відповідальний водій')
    mileage = models.FloatField(default=0, blank=True, verbose_name='Пробіг')
    # ГАБАРИТИ ТА ВАНТАЖОПІДЙОМНІСТЬ
    load_capacity = models.FloatField(verbose_name='Вантажопідйомність',
                                      null=True,
                                      help_text='Вказувати в кілограмах')
    width = models.FloatField(verbose_name='Ширина кузова', null=True, help_text='Вказувати в метрах')
    length = models.FloatField(verbose_name='Довжина кузова', null=True, help_text='Вказувати в метрах')
    height = models.FloatField(verbose_name='Висота кузова', null=True, help_text='Вказувати в метрах')
    # ПАЛИВО
    GASOLINE = 'БЕНЗИН'
    DIESEL = 'ДИЗЕЛЬ'
    GAS = 'ГАЗ'
    TYPE_OF_FUEL = (
        (GASOLINE, 'БЕНЗИН'),
        (DIESEL, 'ДИЗЕЛЬ'),
        (GAS, 'ГАЗ'),
    )
    type_fuel = models.CharField(max_length=20, choices=TYPE_OF_FUEL, verbose_name='Тип палива', null=True)
    tank_size = models.FloatField(null=True, verbose_name='Розмір баку', help_text='В літрах')
    fuel_consumption = models.FloatField(verbose_name='Споживання палива на 100 км', null=True,
                                         help_text='')
    # РЕМОНТ
    is_repair = models.BooleanField(default=False, verbose_name='Авто ремонтується')
    deadline = models.DateField(verbose_name='Коли ремонт буде завершено?', blank=True, null=True)
    what_repair = models.CharField(verbose_name='Що ремонтується?', max_length=200, blank=True, null=True)
    cost = models.PositiveIntegerField(verbose_name='Вартість ремонту', blank=True,
                                       null=True, help_text='В грн.')

    class Meta:
        verbose_name = 'Автомобіль'
        verbose_name_plural = 'Автомобілі'


class Order(models.Model):
    NEW = 'Нова заявка'
    IN_PROCESSING = 'В обробці'
    PREPARE_TO_SHIP = 'Очікує погрузку'
    DONE = 'Завершено'
    STATUS_CHOICES = (
        (NEW, 'Нова заявка'),
        (IN_PROCESSING, 'В обробці'),
        (PREPARE_TO_SHIP, 'Очікує погрузку'),
        (DONE, 'Завершено')
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=NEW, verbose_name='Статус заявки')
    product = models.CharField(max_length=255, null=True, verbose_name='Що бажаєте замовити на доставку?')
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name='Менеджер', null=True)
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, limit_choices_to=Q(is_repair=False),
                            blank=True, null=True, related_name='orders',
                            verbose_name='Автомобіль', unique_for_date='date_trip')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, related_name='orders',
                               null=True, verbose_name='Водій', unique_for_date='date_trip')
    name = models.CharField(max_length=255, verbose_name="Ім'я отримувача", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон отримувача', default='+380 ')
    address = models.CharField(max_length=255, verbose_name='Адреса отримувача',
                               blank=True, null=True,
                               help_text='Область, населений пункт, вулиця, номер будинку та квартири(за потребою)')
    date_trip = models.DateField(default=date.today, verbose_name='Дата доставки')
    total_distance = models.FloatField(
        default=0,
        verbose_name='Загальна відстань рейсу',
        help_text='Вказується в кілометрах'
    )
    amount_trip = models.PositiveSmallIntegerField(verbose_name='Кількість поїздок', default=1)

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'


class RegistrationRefueling(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, verbose_name='Водій')
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, null=True, verbose_name='Автомобіль')
    date_refueling = models.DateField(default=date.today, verbose_name='Дата заправки')
    type_fuel = models.CharField(max_length=20, choices=Cars.TYPE_OF_FUEL,
                                 verbose_name='Тип палива', null=True, )
    amount_fuel = models.FloatField(verbose_name='Кількість палива', help_text='В літрах', null=True)
    price = models.FloatField(verbose_name='Вартість палива', help_text='В грн.', null=True)
    total_price = models.FloatField(verbose_name='Загальна вартість', help_text='В грн.', null=True)
    fuel_check = models.ImageField(upload_to='checks/', null=True, unique=True,
                                   verbose_name='Чек, для бухгалтерії')

    class Meta:
        verbose_name = 'Реєстрація заправки'
        verbose_name_plural = 'Реєстрація заправок'

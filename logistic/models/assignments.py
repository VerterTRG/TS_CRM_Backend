from django.db import models
from logistic.models.drivers import Driver
from logistic.models.trucks import Truck

class Assignment(models.Model):
    id = models.AutoField(primary_key=True,
                          auto_created=True,
                          editable=False,
                          unique_for_year="date_open",
                          verbose_name="Номер"
                          )
    date_open = models.DateField(blank = False, verbose_name="Дата")
    is_open = models.BooleanField(null=False, blank=False, default=True, verbose_name="Действующий")
    driver = models.ForeignKey(Driver, 
                               null=True, 
                               blank=False,
                               on_delete=models.SET_NULL,
                               verbose_name="Водитель")
    truck = models.ForeignKey(Truck, 
                              null=True, 
                              blank=False,
                              on_delete=models.SET_NULL,
                              verbose_name="Автомобиль")
    odometer_start  = models.PositiveSmallIntegerField(verbose_name="Показание одометра перед выездом")
    odometer_end    = models.PositiveSmallIntegerField(blank=True, verbose_name="Показание одометра после возвращения")
    date_close = models.DateField(blank = True, verbose_name="Дата закрытия")

    
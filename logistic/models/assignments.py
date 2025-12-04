from django.db import models
from logistic.models.drivers import Driver
from logistic.models.trucks import Truck
from typing import Optional

class Assignment(models.Model):
    id: models.AutoField = models.AutoField(primary_key=True,
                          auto_created=True,
                          editable=False,
                          unique_for_year="date_open",
                          verbose_name="Номер"
                          )
    date_open: models.DateField = models.DateField(blank = False, verbose_name="Дата")
    is_open: models.BooleanField = models.BooleanField(null=False, blank=False, default=True, verbose_name="Действующий")
    driver: models.ForeignKey = models.ForeignKey(Driver,
                               null=True, 
                               blank=False,
                               on_delete=models.PROTECT,
                               verbose_name="Водитель")
    truck: models.ForeignKey = models.ForeignKey(Truck,
                              null=True, 
                              blank=False,
                              on_delete=models.SET_NULL,
                              verbose_name="Автомобиль")
    odometer_start: models.PositiveSmallIntegerField = models.PositiveSmallIntegerField(blank=True, verbose_name="Показание одометра перед выездом")
    odometer_end: models.PositiveSmallIntegerField = models.PositiveSmallIntegerField(blank=True, verbose_name="Показание одометра после возвращения")
    date_close: models.DateField = models.DateField(blank = True, verbose_name="Дата закрытия")

    class Meta:
        verbose_name = "Путевой лист"
        verbose_name_plural = "Путевые листы"

    def __str__(self) -> str:
        return f"ПЛ №{self.id} от {self.date_open}"

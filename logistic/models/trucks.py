from django.db import models
from typing import Optional

class TypeTruck(models.TextChoices):
    DryVan = "DryVan", "Тентованный"
    Reefer = "Reefer", "Рефрижиратор"
    SideWall = "SideWall", "Бортовой"
    DoubleVan = "DoubleVan", "Сцепка"
    FlatBed = "FlatBed", "Трал"
    Platform = "Platform", "Площадка"
    LowBed = "LowBed", "Низкорамный"

class Truck(models.Model):
    brand: models.CharField = models.CharField(max_length=30, null=True, blank=False, verbose_name="Марка")
    registration: models.CharField = models.CharField(max_length=50, blank=False, unique=True, verbose_name="Гос. номер")
    type_truck: models.CharField = models.CharField(max_length=55, null=True, choices=TypeTruck.choices, blank=False, verbose_name="Тип кузова")
    description: models.CharField = models.CharField(max_length=255, null=True, blank=True, verbose_name="Примечание")

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"

    def __str__(self) -> str:
        return f"{self.brand} {self.registration}"

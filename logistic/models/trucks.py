from django.db import models


class TypeTruck(models.TextChoices):
    DryVan = "DryVan", "Тентованный"
    Reefer = "Reefer", "Рефрижиратор"
    SideWall = "SideWall", "Бортовой"
    DoubleVan = "DoubleVan", "Сцепка"
    FlatBed = "FlatBed", "Трал"
    Platform = "Platform", "Площадка"
    LowBed = "LowBed", "Низкорамный"
    # цистерна, зерновоз, контейнеровоз и т.д. 


class Truck(models.Model):
    brand = models.CharField(max_length=30, null=True, blank=False, verbose_name="Марка") # TODO: Should be created independed model to save brands
    registration = models.CharField(max_length=50, blank=False, unique=True, verbose_name="Гос. номер")
    type_truck = models.CharField(max_length=55, null=True, choices=TypeTruck.choices, blank=False, verbose_name="Тип кузова")
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name="Примечание")
    # single = models.BooleanField(default=False, verbose_name="Грузовик")


# class Trailer(models.Model):
#     # brand = # TODO: Should be created independed model to save brands
#     registration = models.CharField(max_length=30, blank=False, unique=True, verbose_name="Гос. номер")


# class TruckAssignment(models.Model):
#     driver = models.ForeignKey('logistic.Driver', on_delete=models.CASCADE, blank=False, null=False, verbose_name="Водитель")
#     truck = models.ForeignKey('logistic.Truck', on_delete=models.CASCADE, blank=False, null=False, verbose_name="Автомобиль")
#     trailer = models.ForeignKey('logistic.Trailer', on_delete=models.CASCADE, blank=False, null=False, verbose_name="Прицеп")
#     # truck_type = # TODO: Should be assigned type of truck
#     # load_type = # TODO: Should be assigned type of load MULTICHOISE
#     load_max = models.DecimalField(max_digits=3, decimal_places=1, blank=True, verbose_name="Грузоподъемность")
#     capacity_max = models.PositiveSmallIntegerField(max_length=3, blank=True, verbose_name="Объем")
#     description = models.CharField(max_length=255, blank=True, verbose_name="Примечание")
    
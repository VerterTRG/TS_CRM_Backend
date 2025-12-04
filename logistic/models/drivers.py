from django.db import models
from typing import Optional

class TypeID(models.TextChoices):
    Passport = "Passport", "Паспорт"
    PersonalID = "PersonalID", "Удостоверение личности"

class Driver(models.Model):
    name: models.CharField = models.CharField(max_length=255, blank=False, verbose_name="ФИО")
    phone: models.CharField = models.CharField(max_length=255,
                             null=True, 
                             blank=True, 
                             verbose_name="Телефон")
    type_id: models.CharField = models.CharField(max_length=55,
        choices=TypeID.choices,  # Используем определенное перечисление
        verbose_name="Документ")
    data_id: models.CharField  = models.CharField(max_length=255, null=True, blank=True, verbose_name="Реквизиты")
    driver_licence: models.CharField = models.CharField(max_length=30, null=True, blank=True, verbose_name="Водительское удостоверение")

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"

    def __str__(self) -> str:
        return self.name

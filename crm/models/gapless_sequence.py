from django.db import models
from typing import Optional

class GaplessSequence(models.Model):
    """
    Хранит последний выданный номер для последовательности.
    Уникальность гарантируется по (name, tenant, year, user_initials).
    """
    name: models.CharField = models.CharField(max_length=100, verbose_name="Имя последовательности")
    tenant: models.CharField = models.CharField(max_length=100, null=True, blank=True, verbose_name="Тенант")
    year: models.IntegerField = models.IntegerField(null=True, blank=True, verbose_name="Год")
    user_initials: models.CharField = models.CharField(max_length=50, null=True, blank=True, verbose_name="Инициалы пользователя")
    value: models.BigIntegerField = models.BigIntegerField(default=0, verbose_name="Текущее значение")

    class Meta:
        verbose_name = "Нумератор"
        verbose_name_plural = "Нумераторы"
        unique_together = ('name', 'tenant', 'year', 'user_initials')
        indexes = [
            models.Index(fields=['name', 'tenant', 'year', 'user_initials']),
        ]

    def __str__(self) -> str:
        return f"{self.name} / {self.tenant or 'global'} / {self.year or 'any'} / {self.user_initials or 'all'} = {self.value}"

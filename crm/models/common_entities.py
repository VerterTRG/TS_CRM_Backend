from django.conf import settings
from django.db import models
from django.urls import reverse
from typing import Optional, List, TypeVar

T = TypeVar('T', bound='AbstractEntity')

class AbstractEntity(models.Model):

    name: models.CharField = models.CharField(max_length=150, blank=False, verbose_name="Наименование")

    is_group: models.BooleanField = models.BooleanField(default=False, verbose_name="Группа")

    parent: models.ForeignKey = models.ForeignKey(
                                'self', 
                                null=True, 
                                blank=True, 
                                on_delete=models.SET_NULL, 
                                verbose_name="Родитель", 
                                related_name="children", 
                                )

    in_charge: models.ForeignKey = models.ForeignKey(
                                settings.AUTH_USER_MODEL,
                                null=True,
                                on_delete=models.SET_NULL,
                                verbose_name="Ответственный",                            
                                )

    class Meta:
        abstract = True
        verbose_name = "Абстрактная сущность"
        verbose_name_plural = "Абстрактные сущности"
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self) -> str:
        if self.is_group:
            return reverse('list-company') + f'?parent={self.pk}'
        return reverse('detail-company', kwargs={'pk': self.pk})
    
    def get_breadcrumbs(self) -> List['AbstractEntity']:
        breadcrumbs = []
        company = self
        while company:
            breadcrumbs.insert(0, company)
            company = company.parent
        return breadcrumbs

class AbstractEntityMixin:
    pass

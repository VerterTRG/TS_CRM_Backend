from django.db import models
from django.urls import reverse
# from crm.models import User # 'auth.User ???'

class AbstractEntity(models.Model):
    name = models.CharField(max_length=150, blank=False, verbose_name="Наименование")
    isGroup = models.BooleanField(default=False, verbose_name="Группа")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Родитель")
    inCharge = models.ForeignKey('crm.User', null=True, on_delete=models.SET_NULL, verbose_name="Ответственный")

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.name
    
    def __save__(self, *args, **kwargs):
        self.save(*args, **kwargs)

    def get_absolute_url(self):
        if self.isGroup:
            return reverse('list-company') + f'?parent={self.pk}'
        return reverse('detail-company', kwargs={'pk': self.pk})
    
    def get_breadcrumbs(self):
        breadcrumbs = []
        company = self
        while company:
            breadcrumbs.insert(0, company)
            company = company.parent
        return breadcrumbs

class AbstractEntityMixin:
    pass
from django.conf import settings
from django.db import models
from django.urls import reverse
# from crm.models import User # 'auth.User ???'

class AbstractEntity(models.Model):

    name        = models.CharField(max_length=150, blank=False, verbose_name="Наименование")

    is_group     = models.BooleanField(default=False, verbose_name="Группа")

    parent      = models.ForeignKey(
                                'self', 
                                null=True, 
                                blank=True, 
                                on_delete=models.SET_NULL, 
                                verbose_name="Родитель", 
                                related_name="children", 
                                # related_query_name="parent"
                                )
    # creator
    in_charge     = models.ForeignKey(
                                settings.AUTH_USER_MODEL, # TODO: Should be asign app's user when it's be done 'users.User'
                                null=True,
                                on_delete=models.SET_NULL,
                                verbose_name="Ответственный",                            
                                )

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.name
    
    # def __save__(self, *args, **kwargs):
    #     self.save(*args, **kwargs)

    # TODO: Should be created a common util or service to get absolut url by main model
    def get_absolute_url(self):
        if self.is_group:
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
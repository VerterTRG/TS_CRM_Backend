from django.db import models
# from crm.models import User # 'auth.User ???'

class AbstractEntity(models.Model):
    name = models.CharField(max_length=150, blank=False, verbose_name="Наименование")
    isGroup = models.BooleanField(default=False, verbose_name="Группа")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Родитель")
    inCharge = models.ForeignKey('crm.User', null=True, on_delete=models.SET_NULL, verbose_name="Ответственный")

    class Meta:
        abstract = True

    # def __init__(self, *args, **kwargs):
    #     self.__init__(*args, **kwargs)

    
    def __str__(self):
        return self.name
    
    def __save__(self, *args, **kwargs):
        self.save(*args, **kwargs)
    

class AbstractEntityMixin:
    pass
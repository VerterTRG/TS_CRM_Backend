from django.db import models

class Agent(models.Model):
    name = models.CharField(max_length=255, verbose_name="ФИО", blank=True)
    position = models.CharField(max_length=255, verbose_name="Должность", blank=True)
    authority_doc = models.CharField(max_length=255, verbose_name="Документ полномочий", blank=True)
    details = models.CharField(max_length=255, verbose_name="Детали", blank=True)
    company = models.ForeignKey('crm.Company', on_delete=models.CASCADE, related_name='agents', verbose_name="Компания")

    class Meta:
        db_table = "crm_agents"
        verbose_name = "Представитель"
        verbose_name_plural = "Представители"

    def __str__(self):
        return self.name

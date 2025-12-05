from django.db import models

class Agreement(models.Model):
    number = models.CharField(max_length=100, verbose_name="Номер")
    date = models.DateField(verbose_name="Дата", null=True, blank=True)
    company = models.ForeignKey('crm.Company', on_delete=models.CASCADE, related_name='agreements', verbose_name="Компания")

    class Meta:
        db_table = "crm_agreements"
        verbose_name = "Договор"
        verbose_name_plural = "Договоры"

    def __str__(self):
        return f"№ {self.number} от {self.date}"

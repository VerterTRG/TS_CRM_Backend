from django.db import models

class BankAccount(models.Model):
    number = models.CharField(max_length=100, verbose_name="Номер счета")
    bank = models.CharField(max_length=255, verbose_name="Банк")
    bik = models.CharField(max_length=50, verbose_name="БИК")
    cor_number = models.CharField(max_length=100, verbose_name="Корр. счет")
    company = models.ForeignKey('crm.Company', on_delete=models.CASCADE, related_name='bank_accounts', verbose_name="Компания")

    class Meta:
        db_table = "crm_bank_accounts"
        verbose_name = "Банковский счет"
        verbose_name_plural = "Банковские счета"

    def __str__(self):
        return self.number

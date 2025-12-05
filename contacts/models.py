from django.db import models

class Contact(models.Model):

    class Meta:
        db_table = "contact_list"
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    name: models.CharField = models.CharField(max_length=150, blank=False, verbose_name="Имя")
    phone: models.JSONField = models.JSONField(default=list, verbose_name="Телефон", blank=True)
    email: models.JSONField = models.JSONField(default=list, verbose_name="Эл. почта", blank=True)
    comment: models.TextField = models.TextField(blank=True, verbose_name="Комментарий")

    companies = models.ManyToManyField('crm.Company', related_name='contacts', verbose_name="Компании", blank=True)

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"

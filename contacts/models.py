from django.db import models

class Contact(models.Model):

    class Meta:
        db_table = "contact_list"
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    name: models.CharField = models.CharField(max_length=150, blank=False, verbose_name="Имя")
    phone: models.CharField = models.CharField(max_length=150, blank=False, verbose_name="Телефон")
    email: models.CharField = models.CharField(max_length=150, blank=True, verbose_name="Эл. почта")

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} ({self.email})"

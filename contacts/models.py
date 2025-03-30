from django.db import models

class Contact(models.Model):

    class Meta:
        db_table = "contacts_list"

    name        = models.CharField(max_length=150, blank=False, verbose_name="Имя") 
    phone       = models.CharField(max_length=150, blank=True, verbose_name="Телефон") 
    email       = models.CharField(max_length=150, blank=True, verbose_name="Эл. почта") 

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
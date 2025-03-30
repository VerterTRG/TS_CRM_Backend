from django.db import models

class TypeID(models.TextChoices):
    Passport = "Passport", "Паспорт"
    PersonalID = "PersonalID", "Удостоверение личности"

class Driver(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name="ФИО")
    phone = models.CharField(max_length=255,
                             null=True, 
                             blank=True, 
                             verbose_name="Телефон") # TODO: Assign to contacts, shoud be created
    type_id = models.CharField(max_length=55,
        choices=TypeID.choices,  # Используем определенное перечисление
        # null=True,
        # default = TypeID.Passport,
        verbose_name="Документ")
    data_id  = models.CharField(max_length=255, null=True, blank=True, verbose_name="Реквизиты")
    driver_licence = models.CharField(max_length=30, null=True, blank=True, verbose_name="Водительское удостоверение")





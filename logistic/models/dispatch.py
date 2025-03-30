from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator

class PaymentType(models.IntegerChoices):
    NDS             = 1, "с НДС"
    without_NDS     = 2, "без НДС"
    cash            = 3, "Наличные"
    other           = 4, "Прочее"


class Dispatch(models.Model):

    number = models.CharField(verbose_name="Номер",
                              max_length=55,
                              blank=False)
    date = models.DateField(verbose_name="Дата")
    route = models.CharField(verbose_name="Маргрут",
                             max_length=255,
                             blank=False,
                             null=False)
    rate = models.DecimalField(verbose_name="Ставка",
                                max_digits=10,  # Общее максимальное количество цифр (до и после запятой)
                                decimal_places=2, # Количество знаков после запятой
                                validators=[MinValueValidator(Decimal('0.00'))]) # Гарантирует, что значение >= 0.00
    
    payment = models.PositiveSmallIntegerField(verbose_name="Форма оплаты",
                                               max_length=1,
                                               choices=PaymentType.choices,
                                               default=PaymentType.NDS)
    settlement = models.CharField(verbose_name="Порядок оплаты",
                                  max_length=255,
                                  blank=False)

    dateBegin = models.DateField(verbose_name="Дата погрузки")
    dateEnds  = models.DateField(verbose_name="Дата выгрузки")
    contact_tmp = models.CharField(verbose_name="Контакты по заявке",
                                   max_length=255,
                                   default="")
    
    
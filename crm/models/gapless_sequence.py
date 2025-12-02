from django.db import models

# ...existing code...

class GaplessSequence(models.Model):
    """
    Хранит последний выданный номер для последовательности.
    Уникальность гарантируется по (name, tenant, year, user_initials).
    tenant может быть schema_name или любой другой идентификатор тенанта.
    year можно использовать для ежегодной перезагрузки нумерации.
    user_initials — опционально, если требуется персональная (по менеджеру) нумерация.
    """
    name = models.CharField(max_length=100)
    tenant = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    # Добавлено поле для инициалов/идентификатора пользователя (менеджера)
    user_initials = models.CharField(max_length=50, null=True, blank=True)
    value = models.BigIntegerField(default=0)

    class Meta:
        unique_together = ('name', 'tenant', 'year', 'user_initials')
        indexes = [
            models.Index(fields=['name', 'tenant', 'year', 'user_initials']),
        ]

    def __str__(self):
        return f"{self.name} / {self.tenant or 'global'} / {self.year or 'any'} / {self.user_initials or 'all'} = {self.value}"




# Пример модели объекта (Invoice/Contract) с полем для номера
# class Invoice(models.Model):
#     """
#     Пример сущности, которой нужен gapless-номер.
#     number       - целочисленный gapless номер (назначается в транзакции)
#     number_display - форматируемое строковое представление (префикс, год, zero-pad)
#     tenant, year - контекст для уникальности/перезагрузки номера
#     """
#     tenant = models.CharField(max_length=100, null=True, blank=True)  # идентификатор тенанта/схемы
#     year = models.IntegerField(null=True, blank=True)
#     number = models.PositiveIntegerField(null=True, blank=True)  # gapless номер
#     number_display = models.CharField(max_length=50, null=True, blank=True)  # e.g. "INV-2025-000001"
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         # Уникальность гарантируется в пределах tenant+year+number
#         unique_together = ('tenant', 'year', 'number')
#         indexes = [
#             models.Index(fields=['tenant', 'year', 'number']),
#         ]

#     def __str__(self):
#         return self.number_display or f"Invoice #{self.number}"

# Пример использования (в комментарии):
# from django.db import transaction
# with transaction.atomic():
#     number = allocate_gapless_number('invoice', tenant='tenant_42', year=2025)
#     invoice = Invoice.objects.create(
#         tenant='tenant_42',
#         year=2025,
#         number=number,
#         number_display=f"INV-{2025}-{number:06d}",
#         # ... другие поля ...
#     )
# При откате транзакции изменение счетчика и создание Invoice откатятся вместе.
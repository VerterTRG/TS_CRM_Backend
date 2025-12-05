from functools import cached_property
from django.db import models
from crm.models.common_entities import AbstractEntity
from crm.globals.validators import create_digits_validator
from typing import Optional, Any, cast

class Business:
    class Types(models.TextChoices):
        Legal = "Legal", "Юридическое лицо"
        Individual = "Individual", "Индивидуальный предприниматель"
        Person = "Person", "Физическое лицо"
        Government = "Government", "Государственный орган"
        Other = "Other", "Другой"

    """Не используется"""
    class LegalTypes(models.TextChoices):
        OOO = "OOO", "ООО"
        PAO = "PAO", "ПАО"
        AO = "AO", "АО"
        ZAO = "ZAO", "ЗАО"
        NKO = "NKO", ""

class BaseCompany(AbstractEntity):

    class Meta:
        abstract = True

    company_type: models.CharField = models.CharField(verbose_name="Тип контрагента",
        max_length=10,
        choices=Business.Types.choices,
        blank=True,
        null=True
    )

    # Common fields moved from subclasses
    formal_name: models.CharField = models.CharField(max_length=255, blank=True, verbose_name="Полное наименование")

    # Legal / Individual fields
    inn: models.CharField = models.CharField(max_length=12, null=True, blank=True, verbose_name="ИНН", validators=[create_digits_validator('ИНН')])
    ogrn: models.CharField = models.CharField(max_length=15, null=True, blank=True, verbose_name="ОГРН", validators=[create_digits_validator('ОГРН')])

    # Legal fields
    kpp: models.CharField = models.CharField(max_length=9, null=True, blank=True, verbose_name="КПП", validators=[create_digits_validator('КПП')])

    # Person fields
    personal_id: models.CharField = models.CharField(max_length=255, null=True, blank=True, verbose_name="Удостоверение личности")

    # New fields
    address: models.CharField = models.CharField(max_length=255, null=True, blank=True, verbose_name="Адрес")
    mail_address: models.CharField = models.CharField(max_length=255, null=True, blank=True, verbose_name="Почтовый адрес")
    comment: models.TextField = models.TextField(blank=True, verbose_name="Комментарий")

    # Relationships
    main_agreement = models.ForeignKey(
        'crm.Agreement',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='main_agreement_companies',
        verbose_name="Основной договор"
    )
    representative = models.ForeignKey(
        'crm.Agent',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='representative_companies',
        verbose_name="Представитель"
    )
    main_bank_account = models.ForeignKey(
        'crm.BankAccount',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='main_account_companies',
        verbose_name="Основной счет"
    )

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")


    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.is_group and self.company_type:
            raise ValueError("Cannot save a group with a type of business specified. [is_group == True]")
        super().save(*args, **kwargs)

    @property
    def display_name(self) -> str:
        if self.formal_name:
            return self.formal_name
        if self.name:
            return self.name
        return f"Контрагент ID: {self.pk}"

    @cached_property
    def details(self) -> dict:
        return {
            'bank_accounts': self.bank_accounts.all(),
            'contacts': self.contacts.all(),
            'agreements': self.agreements.all(),
            'agents': self.agents.all(),
        }

    def __str__(self) -> str:
        return self.display_name


class CompanyMixin:
    def full_info(self) -> str:
        return self.name # type: ignore
    
    def common_method(self) -> None:
        pass

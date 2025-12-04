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
    
    class BaseExt(models.Model):
        class Meta:
            abstract = True
        
        formal_name: models.CharField = models.CharField(max_length=255, blank=True, verbose_name="Полное наименование")

        def get_display_name(self) -> str:
            return self.formal_name

        def __str__(self) -> str:
            return self.formal_name
    
    class Legal(BaseExt):
        
        inn: models.CharField = models.CharField(max_length=10, null=True, blank=True, unique=True, verbose_name="ИНН", validators=[create_digits_validator('ИНН')])
        kpp: models.CharField = models.CharField(max_length=9, null=True, blank=True, verbose_name="КПП", validators=[create_digits_validator('КПП')])
        ogrn: models.CharField = models.CharField(max_length=13, null=True, blank=True, verbose_name="ОГРН", validators=[create_digits_validator('ОГРН')])

        company: models.OneToOneField = models.OneToOneField('crm.Company', related_name="legal", on_delete=models.CASCADE, verbose_name="Компания")

        class Meta:
            db_table = "crm_business_legals"
            verbose_name = 'Профиль юр. лица'
            verbose_name_plural = 'Профили юр. лиц'


    class Individual(BaseExt):

        inn: models.CharField = models.CharField(max_length=12, null=True, blank=True, unique=True, verbose_name="ИНН", validators=[create_digits_validator('ИНН')])
        ogrn: models.CharField = models.CharField(max_length=15, null=True, blank=True, verbose_name="ОГРН", validators=[create_digits_validator('ОГРН')])

        company: models.OneToOneField = models.OneToOneField('crm.Company', related_name="individual", on_delete=models.CASCADE, verbose_name="Компания")

        class Meta:
            db_table = "crm_business_individuals"
            verbose_name = 'Профиль ИП'
            verbose_name_plural = 'Профили ИП'


    class Person(BaseExt):

        personal_id: models.CharField = models.CharField(max_length=255, null=True, blank=True, verbose_name="Удостоверение личности")

        company: models.OneToOneField = models.OneToOneField('crm.Company', related_name="person", on_delete=models.CASCADE, verbose_name="Компания")

        class Meta:
            db_table = "crm_business_persons"
            verbose_name = 'Профиль физ. лица'
            verbose_name_plural = 'Профили физ. лиц'

    def create_business(self, type_of_business: str, data: Any) -> Any:
        # TODO: This method seems incomplete/placeholder in original code
        business_class = self.Types(type_of_business)
        if business_class:
            return business_class
        else:
            raise ValueError("Unknown Business Type")


class BaseCompany(AbstractEntity):

    class Meta:
        abstract = True

    company_type: models.CharField = models.CharField(verbose_name="Тип контрагента",
        max_length=10,
        choices=Business.Types.choices,
        blank=True,
        null=True
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")


    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.is_group and self.company_type:
            raise ValueError("Cannot save a group with a type of business specified. [is_group == True]")
        super().save(*args, **kwargs)

    
    def get_profile(self) -> Optional[models.Model]:
        """Возвращает связанный профиль в зависимости от типа."""
        if self.company_type == Business.Types.Legal:
            return getattr(self, 'legal', None)
        elif self.company_type == Business.Types.Individual:
            return getattr(self, 'individual', None)
        elif self.company_type == Business.Types.Person:
            return getattr(self, 'person', None)
        return None

    @cached_property
    def info(self) -> Optional[models.Model]:
        return self.get_profile()
    
    @property
    def display_name(self) -> str:
        """Возвращает имя/название из соответствующего профиля."""
        profile = self.info
        if profile and hasattr(profile, 'get_display_name'):
            return cast(Business.BaseExt, profile).get_display_name()
        if self.name:
            return self.name
        return f"Контрагент ID: {self.pk}"

    def __str__(self) -> str:
        return self.display_name


class CompanyMixin:
    def full_info(self) -> str:
        return self.name # type: ignore
    
    def common_method(self) -> None:
        pass

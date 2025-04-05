from django.db import models
from crm.models.common_entities import AbstractEntity
from crm.globals.validators import create_digits_validator



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

        formal_name = models.CharField(max_length=255, blank=True, verbose_name="Полное наименование")
        # Reference to bank account
        # History interactions
    
    class Legal(BaseExt):
 
        inn = models.CharField(max_length=10, null=True, blank=True, unique=True, verbose_name="ИНН", validators=[create_digits_validator('ИНН')])
        kpp = models.CharField(max_length=9, null=True, blank=True, verbose_name="КПП", validators=[create_digits_validator('КПП')])
        ogrn = models.CharField(max_length=13, null=True, blank=True, verbose_name="ОГРН", validators=[create_digits_validator('ОГРН')])

        company = models.OneToOneField('crm.Company', related_name="legal", on_delete=models.CASCADE, null=True)

        def get_display_name(self):
            return self.formal_name

        def __str__(self):
            return self.formal_name

        class Meta:
            db_table = "crm_business_legals"
            verbose_name = ('Профиль юр. лица')
            verbose_name_plural = ('Профили юр. лиц')


    class Individual(BaseExt):

        inn = models.CharField(max_length=12, null=True, blank=True, unique=True, verbose_name="ИНН", validators=[create_digits_validator('ИНН')])
        ogrn = models.CharField(max_length=15, null=True, blank=True, verbose_name="ОГРН", validators=[create_digits_validator('ОГРН')])

        company = models.OneToOneField('crm.Company', related_name="individual", on_delete=models.CASCADE, null=True)

        def get_display_name(self):
        # Можно добавить префикс для ясности
            return f"ИП {self.formal_name}"

        def __str__(self):
            return self.get_display_name()

        class Meta:
            db_table = "crm_business_individuals"
            verbose_name = ('Профиль ИП')
            verbose_name_plural = ('Профили ИП')


    class Person(BaseExt):

        personal_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="Удостоверение личности")

        company = models.OneToOneField('crm.Company', related_name="person", on_delete=models.CASCADE)
    
        def get_display_name(self):
            return self.formal_name

        def __str__(self):
            return self.formal_name

        class Meta:
            db_table = "crm_business_persons"
            verbose_name = ('Профиль физ. лица')
            verbose_name_plural = ('Профили физ. лиц')

    def create_business(self, type_of_business, data):
        business_class = self.Types(type_of_business)
        if business_class:
            return business_class
        else:
            raise ValueError("Unknown Business Type")




class AbstractBusinessEntity(AbstractEntity):

    class Meta:
        abstract = True

    # name, is_group, parent, in_charge
    company_type = models.CharField(verbose_name="Тип контрагента",
        max_length=10,
        choices=Business.Types.choices  # Используем определенное перечисление
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):

        if  self.isGroup and self.company_type:
            raise ValueError("Cannot save a group with a type of business specified. [isGroup == True]")
        
        super().save(*args, **kwargs)

    
    # Вспомогательные методы для удобства
    def get_profile(self):
        """Возвращает связанный профиль в зависимости от типа."""
        if self.company_type == Business.Types.Legal:
            # Используем getattr для безопасности, если профиль еще не создан
            return getattr(self, 'legal', None)
        elif self.company_type == Business.Types.Individual:
            return getattr(self, 'individual', None)
        elif self.company_type == Business.Types.Person:
            return getattr(self, 'person', None)
        return None # На случай появления новых типов без профиля

    @property
    def info(self):
        if hasattr(self, 'legal'):
            return self.legal # type: ignore
        elif hasattr(self, 'individual'):
            return self.individual # type: ignore
        elif hasattr(self, 'person'):
            return self.person # type: ignore
        return None
    
    @property
    def display_name(self):
        """Возвращает имя/название из соответствующего профиля."""
        profile = self.get_profile()
        if profile:
            # Каждый профиль должен иметь метод/свойство для получения имени
            if hasattr(profile, 'get_display_name'):
                return profile.get_display_name()
            elif hasattr(profile, 'name'): # Фолбэк на поле name
                return profile.name
            elif hasattr(profile, 'full_name'): # Фолбэк на поле full_name
                return profile.full_name
        return f"Контрагент ID: {self.id}" # type: ignore # Запасной вариант

    def __str__(self):
        return self.display_name












    

    # @property
    # def typeOfBusiness(self):
    #     return self._typeOfBusiness

    # @typeOfBusiness.setter
    # def typeOfBusiness(self, newType):
    #     if newType not in [choice[0] for choice in Business.Types.choices]:
    #         raise ValueError("Недопустимое значение для business_type")
    #     if not self._copy: 
    #         self._copy = self.__dict__.copy()
    #     # self.__class__ = AbstractBusinessEntity
    #     self._typeOfBusiness = newType
    #     # self.perform_business_specific_action()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.perform_business_specific_action()

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    # def perform_business_specific_action(self):
    #     # Определяем, какой тип бизнеса выбран и назначаем соответствующие методы
    #     if self.typeOfBusiness == Business.Types.Legal:
    #         pass
    #     elif self.typeOfBusiness == Business.Types.Individual:
    #         pass
    #     elif self.typeOfBusiness == Business.Types.Person:
    #         pass
    #     elif self.typeOfBusiness == Business.Types.Government:
    #         pass
    #     elif self.typeOfBusiness == Business.Types.Other:
    #         pass





# Базовый класс миксина для компаний
class CompanyMixin:
    def full_info(self):
        return self.name # type: ignore
    
    def common_method(self):
        pass

# Миксин для компаний, Юридическое лицо
class LegalCompanyMixin(CompanyMixin):
    def full_info(self):
        return "Юридическое лицо: " + super().full_info()
    
    def legal_specific_method(self):
        # Логика для IT-компании
        pass

# Миксин для компаний, Индивидуальный предприниматель
class IndividualCompanyMixin(CompanyMixin):
    def full_info(self):
        return "ИП " + super().full_info()
    
    def individual_specific_method(self):
        # Логика для IT-компании
        pass

# Миксин для компаний, Физическое лицо
class PersonCompanyMixin(CompanyMixin):
    def full_info(self):
        return super().full_info()
    
    def person_specific_method(self):
        # Логика для финансовой компании
        pass

# Миксин для компаний, Государственный орган
class GovernmentCompanyMixin(CompanyMixin):
    class govTypes:
        fns = "FNS", "Налоговая"
        pfr = "PFR", "Орган ПФР"
        fss = "FSS", "Орган ФСС"
        other = "Other", "Прочий"
    
    def full_info(self):
        return super().full_info()
    
    def person_specific_method(self):
        # Логика для гос. органа
        pass

# Миксин для компаний, Другой
class OtherCompanyMixin(CompanyMixin):
    def other_specific_method(self):
        # Логика для другой компании
        pass


# # Декораторы, добавляющие методы миксинов к модели Company
# def add_it_methods(cls):
#     for name, method in ITCompanyMixin.__dict__.items():
#         if callable(method):
#             setattr(cls, name, method)
#     return cls

# def add_finance_methods(cls):
#     for name, method in FinanceCompanyMixin.__dict__.items():
#         if callable(method):
#             setattr(cls, name, method)
#     return cls

# def add_other_methods(cls):
#     for name, method in OtherCompanyMixin.__dict__.items():
#         if callable(method):
#             setattr(cls, name, method)
#     return cls

# Декорируем модель Company соответствующими методами миксинов
# if business_type == BusinessType.IT:
#     Company = add_it_methods(Company)
# elif business_type == BusinessType.Finance:
#     Company = add_finance_methods(Company)
# elif business_type == BusinessType.Other:
#     Company = add_other_methods(Company)
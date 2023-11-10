from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from crm.models.common_entities import AbstractEntity



class Business:

    class Types(models.TextChoices):
        Legal = "Legal", "Юридическое лицо"
        Individual = "Individual", "Индивидуальный предприниматель"
        Person = "Person", "Физическое лицо"
        Government = "Government", "Государственный орган"
        Other = "Other", "Другой"

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
        inn = models.CharField(max_length=12, null=True, blank=True, verbose_name="ИНН")
        # Regerence to bank account
        # History interactions
    
    class Legal(BaseExt):
        class Meta:
            db_table = "crm_business_legals"
        
        kpp = models.CharField(max_length=9, null=True, blank=True, verbose_name="КПП")
        ogrn = models.CharField(max_length=13, null=True, blank=True, verbose_name="ОГРН")

        partner = models.OneToOneField('crm.Company', related_name="legal", on_delete=models.CASCADE, null=True)


    class Individual(BaseExt):
        class Meta:
            db_table = "crm_business_individuals"
        
        ogrn = models.CharField(max_length=15, null=True, blank=True, verbose_name="ОГРН")

        partner = models.OneToOneField('crm.Company', related_name="individual", on_delete=models.CASCADE, null=True)



    class Person(BaseExt):
        class Meta:
            db_table = "crm_business_persons"
        
        personal_id = models.TextField(max_length=255, null=True, blank=True, verbose_name="Удостоверение личности")

        partner = models.OneToOneField('crm.Company', related_name="person", on_delete=models.CASCADE)
    
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
    typeOfBusiness = models.CharField(
        max_length=10,
        choices=Business.Types.choices,  # Используем определенное перечисление
        null=True,
        blank=False,
        verbose_name="Тип контрагента"
    )

    # inn = models.CharField(max_length=12, null=True, blank=True)

    # # Поля для GenericForeignKey
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')

    # # Связь с моделями для каждого типа бизнеса
    # legal_business = GenericRelation(Business.Legal, related_query_name='legal')
    # individual_business = GenericRelation(Business.Individual, related_query_name='individual')
    # person_business = GenericRelation(Business.Person, related_query_name='person')

    def save(self, *args, **kwargs):
        # if self.is_group:
        #     super().save(*args, **kwargs)
        #     return

        # if not self.info:
        #     initialData = {'partner':self,'formal_name':self.name, 'inn':self.inn}
        #     if self.typeOfBusiness == Business.Types.Legal:
        #         business_instance = Business.Legal(**initialData)
        #     elif self.typeOfBusiness == Business.Types.Individual:
        #         business_instance = Business.Individual(**initialData)
        #     elif self.typeOfBusiness == Business.Types.Person:
        #         business_instance = Business.Person(**initialData)
        #     else:
        #         raise ValueError("Invalid type of business")
        #     business_instance.save()
        #     self.content_object = business_instance
        # else:
        #     business_instance = self.content_object
        #     if business_instance is not None:
        #         business_instance.save()
        if  self.isGroup and self.typeOfBusiness:
            raise ValueError("Cannot save a group with a type of business specified. [isGroup == True]")
        
        super().save(*args, **kwargs)

    # @property
    # def info(self):
    #     return self.content_object
    
    @property
    def info(self):
        if hasattr(self, 'legal'):
            return self.legal # type: ignore
        elif hasattr(self, 'individual'):
            return self.individual # type: ignore
        elif hasattr(self, 'person'):
            return self.person # type: ignore
        return None













    

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
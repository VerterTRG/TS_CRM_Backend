from django.db import models
from crm.models.common_business_entities import BaseCompany

# UL, IP, FL, SE (self employed)
class Company(BaseCompany):

    # name, is_group, parent, in_charge, typeOfBusiness, inn, info
    class Meta:
        db_table = "crm_companies"
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"

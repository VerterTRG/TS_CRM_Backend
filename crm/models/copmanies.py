from django.db import models
from crm.models.common_business_entities import AbstractBusinessEntity

# UL, IP, FL, SE (self employed)
class Company(AbstractBusinessEntity):

    # name, is_group, parent, in_charge, typeOfBusiness, inn, info
    class Meta:
        db_table = "crm_companies"


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    # def changeClass(self):
    #     if self.typeOfBusiness == Business.Types.Individual:
    #         pass
    #     elif self.typeOfBusiness == Business.Types.Legal:
    #         pass
    #     elif self.typeOfBusiness == Business.Types.Person:
    #         pass
    #     elif self.typeOfBusiness == Business.Types.Government:
    #         pass
    #     elif self.typeOfBusiness == Business.Types.Other:
    #         pass

    

    # @property
    # def typeOfBusiness(self):
    #     return self._typeOfBusiness

    # @typeOfBusiness.setter
    # def typeOfBusiness(self, newType):
    #     super().__setattr__('typeOfBusiness', newType)
    #     self.changeClass()




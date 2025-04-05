from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.models import inlineformset_factory
from django.forms.utils import ErrorList
from .models import Company, Business
from django.core.validators import RegexValidator

def add_model_validators_to_form_field(form_field, model_field):
    # Добавляем валидаторы, определенные в модели, к полю формы
    for validator in model_field.validators:
        form_field.validators.append(validator)

class BusinessFormMixin():
    def set_read_only(self):
        for field in self.fields.values(): # type: ignore
            field.disabled = True

class CompanyForm(forms.ModelForm, BusinessFormMixin):
    class Meta:
        model = Company
        fields = ['typeOfBusiness', 'name']

# Формы для связанных моделей
class LegalForm(forms.ModelForm, BusinessFormMixin):


    class Meta:
        model = Business.Legal
        exclude = ('partner',)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     # Применяем валидаторы модели к полям формы
    #     for field_name, field in self.fields.items():
    #         model_field = self.Meta.model._meta.get_field(field_name)
    #         add_model_validators_to_form_field(field, model_field)

    #         # Добавляем дополнительные валидаторы, если нужно
    #         if field_name == 'kpp':
    #             field.validators.append(RegexValidator(
    #                 regex='^[0-9]*$',
    #                 message='КПП должен содержать только цифры',
    #                 code='invalid_kpp'
    #             ))

    #         if field_name == 'ogrn':
    #             field.validators.append(RegexValidator(
    #                 regex='^[0-9]*$',
    #                 message='ОГРН должен содержать только цифры',
    #                 code='invalid_ogrn'
    #             ))

    # kpp = forms.CharField(
    #     validators=[
    #         RegexValidator(
    #             regex='^[0-9]*$',
    #             message='КПП должен содержать только цифры',
    #             code='invalid_kpp'
    #         ),
    #         MaxLengthValidator(self.Meta.model._meta.get_field('kpp').max_length),
    #         MinLengthValidator(Meta.model._meta.get_field('kpp').min_length),
    #     ],
    #     required=False
    # )
    # ogrn = forms.CharField(
    #     validators=[
    #         RegexValidator(
    #             regex='^[0-9]*$',
    #             message='ОГРН должен содержать только цифры',
    #             code='invalid_ogrn'
    #         ),
    #         MaxLengthValidator(Meta.model._meta.get_field('kpp').max_length),
    #         MinLengthValidator(Meta.model._meta.get_field('kpp').min_length),
    #     ],
    #     required=False
    # )

    # def __init__(self, *args, **kwargs) -> None:
    #     super().__init__(*args, **kwargs)



class IndividualForm(forms.ModelForm, BusinessFormMixin):
    class Meta:
        model = Business.Individual
        exclude = ('partner',)

class PersonForm(forms.ModelForm, BusinessFormMixin):
    class Meta:
        model = Business.Person
        exclude = ('partner',)

# # Formsets для связанных объектов
# LegalFormSet = inlineformset_factory(Company, Business.Legal, form=LegalForm, extra=1)
# IndividualFormSet = inlineformset_factory(Company, Business.Individual, form=IndividualForm, extra=1)
# PersonFormSet = inlineformset_factory(Company, Business.Person, form=PersonForm, extra=1)
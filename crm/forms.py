from django import forms
from django.forms.models import inlineformset_factory
from .models import Company, Business
from django.core.validators import RegexValidator

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['typeOfBusiness', 'name']

# Формы для связанных моделей
class LegalForm(forms.ModelForm):

    kpp = forms.CharField(
        validators=[
            RegexValidator(
                regex='^[0-9]*$',
                message='КПП должен содержать только цифры',
                code='invalid_kpp'
            ),
        ],
        required=False
    )
    ogrn = forms.CharField(
        validators=[
            RegexValidator(
                regex='^[0-9]*$',
                message='ОГРН должен содержать только цифры',
                code='invalid_ogrn'
            ),
        ],
        required=False
    )

    class Meta:
        model = Business.Legal
        exclude = ('partner',)

class IndividualForm(forms.ModelForm):
    class Meta:
        model = Business.Individual
        exclude = ('partner',)

class PersonForm(forms.ModelForm):
    class Meta:
        model = Business.Person
        exclude = ('partner',)

# # Formsets для связанных объектов
# LegalFormSet = inlineformset_factory(Company, Business.Legal, form=LegalForm, extra=1)
# IndividualFormSet = inlineformset_factory(Company, Business.Individual, form=IndividualForm, extra=1)
# PersonFormSet = inlineformset_factory(Company, Business.Person, form=PersonForm, extra=1)
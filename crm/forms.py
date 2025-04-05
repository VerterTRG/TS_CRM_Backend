from django import forms
# from .models import Company, CompanyType, LegalEntityProfile, SoleProprietorProfile, IndividualProfile
from .models import Company, Business

class CompanyTypeForm(forms.Form):
    """Простая форма для выбора типа компании (для JS)"""
    company_type = forms.ChoiceField(
        choices=Business.Types.choices,
        label=('Тип контрагента'),
        widget=forms.Select(attrs={'id': 'id_company_type_selector'}) # Добавим ID для JS
    )

# --- Формы для Профилей ---
# Убираем поле 'company', так как оно будет установлено во view
class LegalEntityProfileForm(forms.ModelForm):
    class Meta:
        model = Business.Legal
        exclude = ('company',) # Исключаем связь, она установится во view

class IndividualProfileForm(forms.ModelForm):
    class Meta:
        model = Business.Individual
        exclude = ('company',)

class PersonProfileForm(forms.ModelForm):
    class Meta:
        model = Business.Person
        exclude = ('company',)

# --- Комбинированная форма для создания (для удобства передачи в шаблон) ---
# Альтернативно можно передавать формы по отдельности
class CompanyCreateForm:
    """Не настоящая форма Django, а контейнер для других форм"""
    def __init__(self, *args, **kwargs):
        self.type_form = CompanyTypeForm(*args, **kwargs)
        self.legal_form = LegalEntityProfileForm(prefix='legal', *args, **kwargs)
        self.sole_prop_form = IndividualProfileForm(prefix='sole', *args, **kwargs)
        self.individual_form = PersonProfileForm(prefix='ind', *args, **kwargs)

    def is_valid(self, company_type):
        """Проверяет валидность нужной формы профиля"""
        if company_type == Business.Legal:
            return self.legal_form.is_valid()
        elif company_type == Business.Individual:
            return self.sole_prop_form.is_valid()
        elif company_type == Business.Person:
            return self.individual_form.is_valid()
        return False # Неизвестный тип

    def get_profile_form(self, company_type):
        """Возвращает нужную форму профиля"""
        if company_type == Business.Legal:
            return self.legal_form
        elif company_type == Business.Individual:
            return self.sole_prop_form
        elif company_type == Business.Person:
            return self.individual_form
        return None

    # Добавить методы для получения всех форм для рендеринга в шаблоне
    def get_all_forms(self):
         return {
             'type_form': self.type_form,
             'legal_form': self.legal_form,
             'individual_form': self.sole_prop_form,
             'person_form': self.individual_form,
         }
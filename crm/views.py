from django.db import transaction, IntegrityError
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.views.generic.edit import CreateView, UpdateView
from crm.models.common_business_entities import Business

from crm.models.copmanies import Company
from .forms import CompanyForm, IndividualForm, LegalForm, PersonForm #, LegalFormSet, IndividualFormSet, PersonFormSet

class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'crm/company_form.html'
    success_url = '/admin/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['legal_form'] = LegalForm(self.request.POST, prefix='legal')
            context['individual_form'] = IndividualForm(self.request.POST, prefix='individual')
            context['person_form'] = PersonForm(self.request.POST, prefix='person')
        else:
            context['legal_form'] = LegalForm(prefix='legal')
            context['individual_form'] = IndividualForm(prefix='individual')
            context['person_form'] = PersonForm(prefix='person')
        return context

    def form_valid(self, form):
        
        try:
            with transaction.atomic():
                context = self.get_context_data()
                if form.is_valid():
                    self.object = form.save()  

                    # Получаем тип бизнеса из формы
                    type_of_business = form.cleaned_data.get('typeOfBusiness')

                    # Сохраняем связанные формы в зависимости от типа бизнеса
                    if type_of_business == Business.Types.Legal:
                        legal_form = context['legal_form']
                        if not legal_form.is_valid():
                            raise ValidationError('Legal form is not valid')
                        legal = legal_form.save(commit=False)
                        legal.partner = self.object  # Устанавливаем связь с компанией
                        legal.save()

                    elif type_of_business == Business.Types.Individual:
                        individual_form = context['individual_form']
                        if individual_form.is_valid():
                            individual = individual_form.save(commit=False)
                            individual.partner = self.object
                            individual.save()

                    elif type_of_business == Business.Types.Person:
                        person_form = context['person_form']
                        if person_form.is_valid():
                            person = person_form.save(commit=False)
                            person.partner = self.object
                            person.save()

                    # После сохранения основной и связанных форм, перенаправляем пользователя
                    return HttpResponseRedirect(self.get_success_url())

        except (IntegrityError, ValidationError) as e:  # Обработка исключения, связанного с нарушением уникальности
            # Здесь можно обработать исключение, например, добавить сообщение об ошибке
            # form.add_error(None, 'There was a problem with saving: {}'.format(e))
            
            # Если основная форма невалидна, рендерим страницу с ошибками формы
            return self.render_to_response(self.get_context_data(form=form))
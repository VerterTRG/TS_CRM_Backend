from django.db import transaction, IntegrityError
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib import messages

from django.views.generic import ListView, CreateView, UpdateView
from crm.models.common_business_entities import Business

from crm.models.copmanies import Company
from .forms import CompanyForm, IndividualForm, LegalForm, PersonForm #, LegalFormSet, IndividualFormSet, PersonFormSet
from .services import create_company

class CompanyCreateView(CreateView):
    
    model = Company
    form_class = CompanyForm
    template_name = 'crm/company_form.html'
    success_url = '/admin/'
    extra_context = {'title': "Создание контрагента"}

    # sub_form = {
    #     'legal_form': LegalForm,
    #     'individual_form': IndividualForm,
    #     'person_form': PersonForm
    # }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
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

        context = self.get_context_data()

        try:
            with transaction.atomic():
                

                # Получаем тип бизнеса из формы
                type_of_business = form.cleaned_data.get('typeOfBusiness')
            
                if not type_of_business:
                    pass 
                #TODO: 
                # perform raise
                # to provide some message into UI, that typeOfBusiness - required. 
                # Or make the field as required INTO form (if not typeOfBusiness => it's group)
                ####

                company_data = form.cleaned_data

                # Сохраняем связанные формы в зависимости от типа бизнеса
                if type_of_business == Business.Types.Legal:
                    legal_form = context['legal_form']
                    if not legal_form.is_valid():
                        raise ValidationError('Legal form is not valid')
                    
                    ext_compnay_data = legal_form.cleaned_data
                    
                    # legal = legal_form.save(commit=False)
                    # legal.partner = self.object  # Устанавливаем связь с компанией
                    # legal.save()

                elif type_of_business == Business.Types.Individual:
                    individual_form = context['individual_form']
                    if not individual_form.is_valid():
                        raise ValidationError('Individual form is not valid')
                    
                    ext_compnay_data = individual_form.cleaned_data
                    
                    # individual = individual_form.save(commit=False)
                    # individual.partner = self.object
                    # individual.save()

                elif type_of_business == Business.Types.Person:
                    person_form = context['person_form']
                    if not person_form.is_valid():
                        raise ValidationError('Person form is not valid')
                    
                    ext_compnay_data = person_form.cleaned_data
                    
                    # person = person_form.save(commit=False)
                    # person.partner = self.object
                    # person.save()

                else:
                    ext_compnay_data = None

                self.object = create_company(company_data, ext_compnay_data)
                messages.success(self.request, "Компания успешно создана.")

                # После сохранения основной и связанных форм, перенаправляем пользователя
                return HttpResponseRedirect(self.get_success_url())

        except (IntegrityError, ValidationError, ValueError) as e:  # Обработка исключения, связанного с нарушением уникальности
            # Здесь можно обработать исключение, например, добавить сообщение об ошибке
            # form.add_error(None, 'There was a problem with saving: {}'.format(e))
            messages.error(self.request, f"Ошибка при создании компании: {e}")
            # pass

        # В случае исключений, рендерим страницу с ошибками формы
        # return self.render_to_response(self.get_context_data(form=form))
        return self.render_to_response(context)
    
class CompanyListView(ListView):
    model = Company
    # template_name = "crm/company_list.html"
    extra_context = {'title': "Список контрагента"}

    def get_queryset(self):
        group_value = self.request.GET.get('parent', None)
        order = self.request.GET.getlist('orderby', None)
        new_context = Company.objects.filter(
            parent=group_value).order_by(*order)
        return new_context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)

        if 'parent' in self.request.GET:
            context['parent'] = get_object_or_404(Company, pk=self.request.GET.get('parent'))
            # context['parent'] = Company.objects.get(pk=self.request.GET.get('parent'))

        # context["form"] = timezone.now()
        return context


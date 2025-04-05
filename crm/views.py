# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction # Для атомарного сохранения Company + Profile
from django.http import HttpResponseBadRequest

from .models import Company, Business
from .forms import (
    CompanyTypeForm, LegalEntityProfileForm, IndividualProfileForm, PersonProfileForm, CompanyCreateForm
)

class CompanyListView(ListView):
    model = Company
    template_name = 'crm/company_list_new.html' # Укажите свой путь
    context_object_name = 'companies'

class CompanyDetailView(DetailView):
    model = Company
    template_name = 'crm/company_detail_new.html' # Укажите свой путь
    context_object_name = 'company'

    def get_queryset(self):
        # Оптимизируем запрос, подгружая нужные профили
        return super().get_queryset().select_related(
            'legal', 'individual', 'person'
        )

# --- Создание контрагента ---
class CompanyCreateView(View):
    template_name = 'crm/company_form_new.html' # Укажите свой путь

    def get(self, request, *args, **kwargs):
        # Передаем все формы в шаблон для рендеринга (JS будет их скрывать/показывать)
        forms_container = CompanyCreateForm()
        context = {'forms': forms_container.get_all_forms()}
        return render(request, self.template_name, context)

    @transaction.atomic # Гарантируем, что Company и Profile сохранятся вместе или никак
    def post(self, request, *args, **kwargs):
        # 1. Получаем выбранный тип
        type_form = CompanyTypeForm(request.POST)
        if not type_form.is_valid():
            # Если тип не выбран или невалиден - ошибка
            forms_container = CompanyCreateForm(request.POST) # Передаем данные для отображения ошибок
            context = {'forms': forms_container.get_all_forms()}
            # Можно добавить сообщение об ошибке
            return render(request, self.template_name, context, status=400)

        company_type = type_form.cleaned_data['company_type']

        # 2. Создаем экземпляр Company
        company = Company(company_type=company_type)
        # Здесь можно добавить сохранение общих полей из request.POST, если они есть

        # 3. Инициализируем и валидируем нужную форму профиля
        profile_form = None
        if company_type == Business.Types.Legal:
            profile_form = LegalEntityProfileForm(request.POST, prefix='legal')
        elif company_type == Business.Types.Individual:
            profile_form = IndividualProfileForm(request.POST, prefix='sole')
        elif company_type == Business.Types.Person:
            profile_form = PersonProfileForm(request.POST, prefix='ind')
        else:
            # Неизвестный тип - ошибка
             return HttpResponseBadRequest("Invalid company type selected.")

        if profile_form and profile_form.is_valid():
            # Сохраняем Company только если форма профиля валидна
            company.save()
            # Сохраняем профиль, связывая его с Company
            profile = profile_form.save(commit=False)
            profile.company = company # Устанавливаем связь
            profile.save()
            return redirect(reverse_lazy('company-detail', kwargs={'pk': company.pk})) # Или на список
        else:
            # Если форма профиля не валидна, рендерим страницу заново со всеми ошибками
            forms_container = CompanyCreateForm(request.POST)
            context = {
                'forms': forms_container.get_all_forms(),
                'selected_type': company_type # Передаем выбранный тип для JS
            }
            return render(request, self.template_name, context, status=400)


# --- Редактирование контрагента ---
class CompanyUpdateView(View):
    template_name = 'crm/company_update_form_new.html' # Укажите свой путь

    def get_company_and_profile(self, pk):
        """Получает компанию и ее профиль"""
        company = get_object_or_404(
            Company.objects.select_related(
                'legal', 'individual', 'person'
            ),
            pk=pk
        )
        profile = company.get_profile()
        return company, profile

    def get_profile_form_class(self, company_type):
        """Возвращает класс формы для типа компании"""
        if company_type == Business.Types.Legal:
            return LegalEntityProfileForm
        elif company_type == Business.Types.Individual:
            return IndividualProfileForm
        elif company_type == Business.Types.Person:
            return PersonProfileForm
        return None

    def get(self, request, pk, *args, **kwargs):
        company, profile = self.get_company_and_profile(pk)
        ProfileFormClass = self.get_profile_form_class(company.company_type)

        if not ProfileFormClass:
             # Обработка случая, если тип некорректен или нет формы для него
             return HttpResponseBadRequest("Cannot edit company: unknown type or profile form missing.")

        # Форма для типа здесь не нужна, т.к. тип не меняем (обычно)
        profile_form = ProfileFormClass(instance=profile)
        # Можно добавить форму для редактирования общих полей Company, если они есть

        context = {
            'company': company,
            'profile_form': profile_form,
            # 'company_form': company_edit_form (если есть)
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, pk, *args, **kwargs):
        company, profile = self.get_company_and_profile(pk)
        ProfileFormClass = self.get_profile_form_class(company.company_type)

        if not ProfileFormClass:
             return HttpResponseBadRequest("Cannot save company: unknown type or profile form missing.")

        profile_form = ProfileFormClass(request.POST, instance=profile)
        # company_form = CompanyEditForm(request.POST, instance=company) # Если есть

        # Проверяем валидность ТОЛЬКО формы профиля (и формы Company, если есть)
        if profile_form.is_valid(): # and company_form.is_valid():
            # company_form.save()
            profile_form.save()
            # Обновляем updated_at в Company вручную, если нужно
            company.save(update_fields=['updated_at'])
            return redirect(reverse_lazy('company-detail', kwargs={'pk': company.pk}))
        else:
            # Если форма не валидна, показываем ошибки
            context = {
                'company': company,
                'profile_form': profile_form,
                # 'company_form': company_form,
            }
            return render(request, self.template_name, context, status=400)

class CompanyDeleteView(DeleteView):
    model = Company
    # Имя шаблона, который запросит подтверждение удаления
    template_name = 'crm/company_confirm_delete.html'
    # Имя переменной в контексте шаблона подтверждения
    context_object_name = 'company' # или 'object' по умолчанию
    # URL, на который перенаправить пользователя после успешного удаления
    success_url = reverse_lazy('company-list') # Перенаправляем на список компаний

    # Вы можете добавить сюда проверку прав доступа, переопределив метод dispatch или post,
    # например:
    # from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
    # class CompanyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    #     # ...
    #     def test_func(self):
    #         # Пример: только суперпользователь может удалять
    #         return self.request.user.is_superuser
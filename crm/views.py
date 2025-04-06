# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction # Для атомарного сохранения Company + Profile
from django.http import HttpResponseBadRequest
from django.contrib import messages # Импортируем для сообщений пользователю
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Company, Business
from .forms import (
    CompanyForm, CompanyTypeForm, LegalEntityProfileForm, IndividualProfileForm, PersonProfileForm, CompanyCreateForm
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
class CompanyCreateView(LoginRequiredMixin, View):
    template_name = 'crm/company_form_new.html' # Укажите свой путь

    def get(self, request, *args, **kwargs):
        # Создаем пустой контейнер для первого отображения формы
        form_container = CompanyCreateForm()
        # Передаем словарь форм в контекст
        context = {'forms': form_container.get_all_forms()}
        return render(request, self.template_name, context)

    @transaction.atomic # Оставляем транзакцию для атомарности
    def post(self, request, *args, **kwargs):
        # 1. Создаем ОДИН экземпляр контейнера со всеми данными из POST
        # Префиксы, указанные в __init__ контейнера, помогут Django
        # правильно разобрать данные по формам
        form_container = CompanyCreateForm(request.POST)

        # 2. Определяем выбранный тип компании
        # Лучше взять его из данных формы выбора типа внутри контейнера
        selected_company_type = None
        # Сначала проверим валидность самой формы выбора типа
        if form_container.type_form.is_valid():
             selected_company_type = form_container.type_form.cleaned_data.get('company_type')
        else:
             # Если тип не выбран или невалиден - сразу рендерим форму с ошибкой
             messages.error(request, "Пожалуйста, выберите корректный тип контрагента.")
             context = {'forms': form_container.get_all_forms()}
             return render(request, self.template_name, context, status=400)

        # Если тип не определился (хотя is_valid прошел?), на всякий случай
        if not selected_company_type:
             messages.error(request, "Не удалось определить тип контрагента.")
             context = {'forms': form_container.get_all_forms()}
             return render(request, self.template_name, context, status=400)

        # 3. Валидируем контейнер
        # Метод is_valid контейнера должен вызывать is_valid() для company_form
        # и для нужной формы профиля (legal_form, individual_form или person_form)
        if form_container.is_valid(selected_company_type):
            # 4. Сохраняем базовую компанию
            # Используем company_form из контейнера
            try:
                company = form_container.company_form.save(commit=False)
                # Устанавливаем тип компании (он не был полем в CompanyForm)
                company.company_type = selected_company_type
                company.save() # Сохраняем Company в БД

                # 5. Сохраняем связанный профиль
                # Используем get_profile_form для получения нужной формы из контейнера
                profile_form = form_container.get_profile_form(selected_company_type)
                if profile_form: # Убедимся, что форма профиля найдена
                    profile = profile_form.save(commit=False)
                    profile.company = company # Устанавливаем связь с созданной Company
                    profile.save() # Сохраняем профиль в БД
                else:
                    # Этого не должно произойти, если is_valid прошел, но для безопасности
                    raise ValueError("Не удалось найти форму профиля для указанного типа.")

                # 6. Опционально: Добавляем сообщение об успехе
                messages.success(request, f"Контрагент '{company.name}' успешно создан.")

                # 7. Перенаправляем на страницу успеха (замените 'crm:company_list' на ваш URL)
                return redirect('crm:company-list') # TODO: Укажите правильный URL name

            except Exception as e:
                # Ловим возможные ошибки при сохранении
                messages.error(request, f"Произошла ошибка при сохранении: {e}")
                # Возвращаем пользователя к форме с данными, но без сохранения
                context = {'forms': form_container.get_all_forms()}
                return render(request, self.template_name, context, status=500)

        else:
            # 8. Если валидация контейнера не прошла
            # Просто рендерим шаблон снова. Экземпляр form_container уже содержит
            # все нужные формы с данными И ошибками валидации.
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
            context = {'forms': form_container.get_all_forms()}
            return render(request, self.template_name, context, status=400) # Bad request


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
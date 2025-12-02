"""from django.db import transaction
from .models import Company, Business

@transaction.atomic
def create_company(company_data, ext_data):
    # здесь может быть логика по созданию объекта Company
    # и связанных с ним объектов Legal или Individual

    typeOfBusiness = company_data['typeOfBusiness']

    if typeOfBusiness and not ext_data:
        raise ValueError(f'Для модели Company с типом - {typeOfBusiness}, обработчик создания чрез контроллер еще не определен.')
    
    ext_class = getattr(Business, typeOfBusiness)
    if not ext_class:
        raise NameError(f'Для модели Company с типом - {typeOfBusiness}, модель не определена.')

    # Создание основного объекта Company
    company = Company.objects.create(**company_data)

    # Создание связанной модели Company
    ext_model = ext_class.objects.create(partner=company, **ext_data)


    return company

def update_company(company_id, company_data):
    # логика обновления информации о компании
    pass"""

from django.db.models import QuerySet, Q
from multiprocessing.managers import BaseManager
from django.db import transaction
from django.contrib.auth import get_user_model
from typing import Optional, Union
from ninja.errors import HttpError

import logging # <-- Или используем logging вместо print

logger = logging.getLogger(__name__) # Настраиваем логгер

# Импортируем всё необходимое
from .models import Company, Business
from .schemas import CompanyInputUnion, LegalCompanyInputSchema, IndividualCompanyInputSchema, PersonCompanyInputSchema

User = get_user_model()

@transaction.atomic
def create_company(payload: CompanyInputUnion) -> Company:
    """
    Сервисная функция для создания Company и связанного Profile.
    Выполняется в атомарной транзакции.
    """
    print(f"Сервис: Запрос на создание {payload.company_type}")

    # 1. Подготовка связанных объектов (Parent, InCharge)
    parent_company = None
    if payload.parent:
        try:
            # Ищем родителя ТОЛЬКО среди групп
            parent_company = Company.objects.filter(is_group=True).get(pk=payload.parent)
        except Company.DoesNotExist:
            raise HttpError(400, f"Родительская группа с ID {payload.parent} не найдена.")

    in_charge_user = None
    if payload.in_charge_id:
        try:
            in_charge_user = User.objects.get(pk=payload.in_charge_id)
        except User.DoesNotExist:
             raise HttpError(400, f"Ответственный пользователь с ID {payload.in_charge_id} не найден.")

    # 2. Проверка: Нельзя создавать группу с типом бизнеса
    if payload.is_group and payload.company_type:
         raise HttpError(400, "Нельзя создавать группу ('is_group'=true) с указанием типа контрагента ('company_type').")

    # 3. Создаем Company
    company = Company.objects.create(
        name=payload.name,
        is_group=payload.is_group,
        parent=parent_company,
        in_charge=in_charge_user,
        company_type=payload.company_type if not payload.is_group else None # Тип только если не группа
    )
    print(f"Сервис: Company создан, ID: {company.id}") # type: ignore

    # 4. Создаем Профиль, только если это не группа
    if not company.is_group:
        profile_info_data = payload.info.model_dump(exclude_unset=True) if payload.info else {}
        print(f"Сервис: Данные профиля: {profile_info_data}")

        if isinstance(payload, LegalCompanyInputSchema):
            profile = Business.Legal.objects.create(company=company, **profile_info_data)
            print(f"Сервис: LegalEntityProfile создан, ID: {profile.pk}")
        elif isinstance(payload, IndividualCompanyInputSchema):
            profile = Business.Individual.objects.create(company=company, **profile_info_data)
            print(f"Сервис: IndividualProfile создан, ID: {profile.pk}")
        elif isinstance(payload, PersonCompanyInputSchema):
             # Убедимся, что profile_info_data не пустой, если для PersonInfoSchema есть обязательные поля
            profile = Business.Person.objects.create(company=company, **profile_info_data)
            print(f"Сервис: PersonProfile создан, ID: {profile.pk}")
        else:
            # Эта ветка не должна выполниться из-за проверки Pydantic/Ninja
            raise ValueError(f"Неподдерживаемый тип payload в сервисе: {type(payload)}")

    return company

def get_list_companies(
    *,
    search: Optional[str] = None,
    company_type: Optional[str] = None,
    is_group: Optional[bool] = None,
    # Добавьте другие фильтры по необходимости
    # responsible_user: Optional[User] = None,
    order_by: str = 'name' # Сортировка по умолчанию
) -> QuerySet[Company]: # Более точный тип возврата
    """
    Возвращает QuerySet для списка компаний с возможностью фильтрации и сортировки.

    Предполагается, что функция вызывается в контексте с уже установленной схемой тенанта.
    Пагинация должна применяться вызывающим кодом (например, в API view).
    """
    # Начинаем с базового менеджера (будет работать с текущей активной схемой)
    queryset = Company.objects.all()

    # Применяем фильтры, если они переданы
    if search:
        # Пример поиска по имени (регистронезависимый)
        # queryset = queryset.filter(name__icontains=search)
        # Можно добавить поиск по другим полям через Q-объекты:
        queryset = queryset.filter(Q(name__icontains=search) | Q(legal__inn__icontains=search) | Q(individual__inn__icontains=search)) # Пример
    if company_type:
        queryset = queryset.filter(company_type=company_type)
    if is_group is not None: # Важно проверять на None, а не просто if is_group:
        queryset = queryset.filter(is_group=is_group)
    # if responsible_user:
    #     queryset = queryset.filter(in_charge=responsible_user) # Пример

    # Применяем оптимизацию (select/prefetch related) ПОСЛЕ фильтрации
    queryset = queryset.select_related('parent', 'in_charge').prefetch_related(
        'legal', 'individual', 'person' # Убедитесь, что имена правильные
    )

    # Применяем сортировку
    if order_by:
        # ВАЖНО: Валидировать поля для сортировки! (см. ниже)
        allowed_ordering_fields = get_allowed_ordering_fields() # Получаем список разрешенных полей
        validated_fields = validate_ordering_string(order_by, allowed_ordering_fields)
        if validated_fields:
            queryset = queryset.order_by(*validated_fields) # Передаем РАСПАКОВАННЫЙ список полей
        else:
            # Если переданы невалидные поля, применяем сортировку по умолчанию
             queryset = queryset.order_by('name') # Пример по умолчанию
    else:
        # Сортировка по умолчанию, если параметр ordering не передан
        queryset = queryset.order_by('name') # Пример по умолчанию

    # Возвращаем QuerySet, НЕ вызывая .all()
    return queryset

# --- Функции Валидации Сортировки (разместите где удобно) ---
def get_allowed_ordering_fields() -> set:
    """Возвращает множество имен полей модели Company, по которым разрешена сортировка."""
    # Перечислите ЗДЕСЬ поля вашей модели Company, по которым можно сортировать
    return {'id', 'name', 'company_type', 'is_group', 'created_at', 'updated_at'}
    # Можно добавить поля связанных моделей через '__', например 'parent__name',
    # но только если вы ХОТИТЕ разрешить сортировку по ним и добавили их в allowed_fields

def validate_ordering_string(ordering_string: str, allowed_fields: set) -> list:
    """
    Проверяет строку сортировки, возвращает список валидных полей для order_by.
    Поддерживает префикс '-' и сортировку по нескольким полям через ','.
    """
    validated_fields = []
    if not ordering_string:
        return []

    fields = [field.strip() for field in ordering_string.split(',')]
    for field in fields:
        direction = ''
        field_name = field
        if field.startswith('-'):
            direction = '-'
            field_name = field[1:]

        # Проверяем, разрешено ли поле (без учета направления)
        if field_name in allowed_fields:
            validated_fields.append(direction + field_name)
        else:
            logger.warning(f"Попытка сортировки по неразрешенному полю: '{field_name}' (из строки '{field}') - проигнорировано.")
            # Можно здесь генерировать ошибку или просто игнорировать

    return validated_fields


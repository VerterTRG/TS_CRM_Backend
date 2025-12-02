# api.py
from django.shortcuts import get_object_or_404
from ninja import Query, Path, Schema, Body, Router
from ninja_extra import api_controller, route, ControllerBase
from drf_spectacular.utils import extend_schema
from ninja.errors import HttpError
from typing import List, Optional
import re
from django.db import IntegrityError

from ninja_extra import api_controller

from crm.models.copmanies import Company

from .schemas import CompanyFilterSchema, CompanyInputUnion, CompanyOutputSchema # Наши схемы
from .services import create_company, get_list_companies # Наш сервис

from django.db import connection # <-- Импортируем объект соединения
import logging # <-- Или используем logging вместо print

logger = logging.getLogger(__name__) # Настраиваем логгер


router = Router()

@router.get("/hello", auth=None) # Используем GET для простоты
@extend_schema(summary="Простой тестовый эндпоинт CRM") # Простой extend_schema
def simple_crm_test(request):
    """Просто возвращает приветствие из CRM."""
    return {"message": "Hello from CRM API!"}


class ErrorSchema(Schema):
    detail: str
    field_errors: Optional[dict] = None



@api_controller("crm/company", tags=["Companies"])
class CompanyController(ControllerBase):

    @route.post(
        "/create",
        tags=["Companies"],
        summary="Создает нового контрагента", # Используйте параметр summary
        # Опционально: Укажите схемы ответа для разных кодов
        response={
            201: CompanyOutputSchema, # Схема успешного ответа
            400: ErrorSchema,         # Схема для ошибок валидации/HttpError
            500: ErrorSchema          # Схема для внутренних ошибок
        }
    )
    def create_company_endpoint(self, request, payload: CompanyInputUnion = Body(...)): # type: ignore
        """
        Создает нового контрагента (Компанию с профилем или Группу).
        Структура поля 'info' обязательна и зависит от 'company_type'.
        Для 'is_group'=true поле 'info' null, 'company_type' так же должен быть null.
        """
        try:
            # Вызываем сервис, передаем провалидированные данные
            print(f"API: Получен запрос на создание {request.body.decode('utf-8')}")
            new_company = create_company(payload)
            # Возвращаем созданный объект, он будет сериализован через CompanyOutputSchema
            return 201, new_company
        except HttpError as e:
            # Перехватываем ожидаемые ошибки от сервиса (400)
            return e.status_code, {"detail": str(e)}
        except IntegrityError as e:
            # Пытаемся извлечь поле из сообщения PostgreSQL: "Key (inn)=(123) already exists."
            msg = str(e)
            m = re.search(r'Key \((?P<field>[\w_]+)\)=\((?P<value>.+?)\)', msg)
            if m:
                field = m.group('field')
                value = m.group('value')
                logger.info(f"DB IntegrityError on field {field} value {value}")
                return 400, {"detail": f"Duplicate value for field '{field}'", "field_errors": {field: "already exists"}}
            # Если не удалось распарсить — вернуть общий ответ с текстом ошибки
            logger.exception("IntegrityError при создании Company")
            return 400, {"detail": "Database integrity error", "field_errors": {"__all__": msg}}
        except Exception as e:
            # Логируем непредвиденные ошибки!
            logger.exception(f"Непредвиденная ошибка API: {e}")
            return 500, {"detail": "Внутренняя ошибка сервера."}

    # Добавьте другие эндпоинты (GET list, GET detail, PUT, DELETE) при необходимости
    # Например, GET list:
    @route.get(
            "/list",
            tags=["Companies"],
            summary="Получает список контрагентов", # Используйте параметр summary
        # Опционально: Укажите схемы ответа для разных кодов
        response={
            200: List[CompanyOutputSchema], # Схема успешного ответа
            400: ErrorSchema,         # Схема для ошибок валидации/HttpError
            500: ErrorSchema          # Схема для внутренних ошибок
        } 
    )
    def list_companies(self, request, filters: CompanyFilterSchema = Query(...)): # type: ignore
        """
        Возращает список контрагентов (Компанию с профилем или Группу).
        Структура поля 'info' обязательна и зависит от 'company_type'.
        Для 'is_group'=true поле 'info' null, 'company_type' так же null.
        """
        logger.warning("--- DEBUG: BEFORE Company.objects.all() ---") # Используем warning для заметности
        logger.warning(f"connection.schema_name = {getattr(connection, 'schema_name', 'N/A (Attribute missing?)')}")
        qs = get_list_companies(**filters.dict(exclude_none=True))
        return qs

    @route.get(
        "/{id}", # Используем /company (единственное число) для получения одного объекта
        tags=["Companies"],
        summary="Получает одного контрагента по ID",
        response={
            200: CompanyOutputSchema, # Успешный ответ - ОДИН объект CompanyOutputSchema
            404: ErrorSchema,         # Ошибка, если объект не найден
            500: ErrorSchema       # Можно оставить для необработанных ошибок
        }
    )
    # @set_tenant_schema_decorator # <--- Применяем декоратор, если НЕТ зависимости на Router/API
    def get_company_by_id(self, request, company_id: int = Path(..., alias="id", description="ID контрагента для поиска")): # type: ignore
        """
        Возвращает детали одного контрагента по его ID (pk).
        ID передается как query параметр '?id=<number>'.
        """
        logger.info(f"VIEW CRM: get_company_by_id: schema={connection.schema_name}, requested_id={company_id}")

        # Используем get_object_or_404 для получения объекта или автоматического ответа 404
        qs = Company.objects.select_related('parent', 'in_charge').prefetch_related('legal', 'individual', 'person')
        company = get_object_or_404(qs, pk=company_id)

        return company
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

from crm.models.companies import Company

from .schemas import (
    CompanyFilterSchema, CompanyInputUnion, CompanyOutputSchema, CompanyFullOutputSchema,
    AgreementSchema, AgreementInputSchema, AgreementUpdateSchema,
    AgentSchema, AgentInputSchema, AgentUpdateSchema,
    BankAccountSchema, BankAccountInputSchema, BankAccountUpdateSchema
)
from .services import (
    create_company, get_list_companies,
    create_agreement, update_agreement,
    create_agent, update_agent,
    create_bank_account, update_bank_account
)

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

# --- Helpers ---

def handle_integrity_error(e: IntegrityError):
    # Пытаемся извлечь поле из сообщения PostgreSQL: "Key (inn)=(123) already exists."
    msg = str(e)
    m = re.search(r'Key \((?P<field>[\w_]+)\)=\((?P<value>.+?)\)', msg)
    if m:
        field = m.group('field')
        value = m.group('value')
        logger.info(f"DB IntegrityError on field {field} value {value}")
        return 400, {"detail": f"Duplicate value for field '{field}'", "field_errors": {field: "already exists"}}
    # Если не удалось распарсить — вернуть общий ответ с текстом ошибки
    logger.exception("IntegrityError")
    return 400, {"detail": "Database integrity error", "field_errors": {"__all__": msg}}

# --- Controllers ---

@api_controller("crm/company", tags=["Companies"])
class CompanyController(ControllerBase):

    @route.post(
        "/create",
        tags=["Companies"],
        summary="Создает нового контрагента", # Используйте параметр summary
        response={
            201: CompanyOutputSchema,
            400: ErrorSchema,
            500: ErrorSchema
        }
    )
    def create_company_endpoint(self, request, payload: CompanyInputUnion = Body(...)): # type: ignore
        """
        Создает нового контрагента (Компанию с профилем или Группу).
        """
        try:
            new_company = create_company(payload)
            return 201, new_company
        except HttpError as e:
            return e.status_code, {"detail": str(e)}
        except IntegrityError as e:
            return handle_integrity_error(e)
        except Exception as e:
            logger.exception(f"Unexpected error API: {e}")
            return 500, {"detail": "Internal Server Error."}

    @route.get(
            "/list",
            tags=["Companies"],
            summary="Получает список контрагентов",
        response={
            200: List[CompanyOutputSchema],
            400: ErrorSchema,
            500: ErrorSchema
        } 
    )
    def list_companies(self, request, filters: CompanyFilterSchema = Query(...)): # type: ignore
        """
        Возращает список контрагентов (Компанию с профилем или Группу).
        """
        qs = get_list_companies(**filters.dict(exclude_none=True))
        return qs

    @route.get(
        "/{id}",
        tags=["Companies"],
        summary="Получает одного контрагента по ID",
        response={
            200: CompanyFullOutputSchema,
            404: ErrorSchema,
            500: ErrorSchema
        }
    )
    def get_company_by_id(self, request, company_id: int = Path(..., alias="id", description="ID контрагента для поиска")): # type: ignore
        """
        Возвращает детали одного контрагента по его ID (pk).
        Включает полную информацию: банковские счета, контакты, договоры, представители.
        """
        qs = Company.objects.select_related('parent', 'in_charge') \
            .prefetch_related(
                'bank_accounts',
                'contacts',
                'agreements',
                'agents'
            )
        company = get_object_or_404(qs, pk=company_id)
        return company

@api_controller("crm/agreement", tags=["Agreements"])
class AgreementController(ControllerBase):

    @route.post("/create", response={201: AgreementSchema, 400: ErrorSchema})
    def create(self, request, payload: AgreementInputSchema):
        try:
            return 201, create_agreement(payload)
        except Exception as e:
             return 400, {"detail": str(e)}

    @route.put("/{id}/update", response={200: AgreementSchema, 404: ErrorSchema, 400: ErrorSchema})
    def update(self, request, id: int, payload: AgreementUpdateSchema):
        try:
            return update_agreement(id, payload)
        except Exception as e:
            return 400, {"detail": str(e)}

@api_controller("crm/agent", tags=["Agents"])
class AgentController(ControllerBase):

    @route.post("/create", response={201: AgentSchema, 400: ErrorSchema})
    def create(self, request, payload: AgentInputSchema):
        try:
            return 201, create_agent(payload)
        except Exception as e:
             return 400, {"detail": str(e)}

    @route.put("/{id}/update", response={200: AgentSchema, 404: ErrorSchema, 400: ErrorSchema})
    def update(self, request, id: int, payload: AgentUpdateSchema):
        try:
            return update_agent(id, payload)
        except Exception as e:
            return 400, {"detail": str(e)}

@api_controller("crm/bank_account", tags=["BankAccounts"])
class BankAccountController(ControllerBase):

    @route.post("/create", response={201: BankAccountSchema, 400: ErrorSchema})
    def create(self, request, payload: BankAccountInputSchema):
        try:
            return 201, create_bank_account(payload)
        except Exception as e:
             return 400, {"detail": str(e)}

    @route.put("/{id}/update", response={200: BankAccountSchema, 404: ErrorSchema, 400: ErrorSchema})
    def update(self, request, id: int, payload: BankAccountUpdateSchema):
        try:
            return update_bank_account(id, payload)
        except Exception as e:
            return 400, {"detail": str(e)}

from django.db.models import QuerySet, Q
from django.db import transaction, models
from django.contrib.auth import get_user_model
from typing import Optional, Union, Any, Type
from ninja.errors import HttpError
from ninja import Schema
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)

# Imports
from .models import Company, Business, Agreement, Agent, BankAccount
from .schemas import (
    CompanyInputUnion,
    LegalCompanyInputSchema,
    IndividualCompanyInputSchema,
    PersonCompanyInputSchema,
    AgreementInputSchema, AgreementUpdateSchema,
    AgentInputSchema, AgentUpdateSchema,
    BankAccountInputSchema, BankAccountUpdateSchema
)

User = get_user_model()

# --- Company Services ---

@transaction.atomic
def create_company(payload: CompanyInputUnion) -> Company:
    """
    Creates a new Company.
    """
    print(f"Service: Request to create {payload.company_type}")

    # 1. Prepare related objects (Parent, InCharge)
    parent_company = None
    if payload.parent:
        try:
            parent_company = Company.objects.filter(is_group=True).get(pk=payload.parent)
        except Company.DoesNotExist:
            raise HttpError(400, f"Parent group with ID {payload.parent} not found.")

    in_charge_user = None
    if payload.in_charge_id:
        try:
            in_charge_user = User.objects.get(pk=payload.in_charge_id)
        except User.DoesNotExist:
             raise HttpError(400, f"User with ID {payload.in_charge_id} not found.")

    # 2. Validation: Cannot create group with company_type
    if payload.is_group and payload.company_type:
         raise HttpError(400, "Cannot create a group ('is_group'=true) with 'company_type' specified.")

    # 3. Create Company (Flat model)
    # Extract common fields
    common_data = payload.dict(exclude={'info', 'company_type', 'is_group', 'parent', 'in_charge_id'})

    # Extract specific fields from payload depending on type (if we were using old way, but now it's flat)
    # Actually, pydantic model dump includes all fields.
    # We need to map payload fields to model fields.

    company_data = payload.dict(exclude={'is_group', 'parent', 'in_charge_id'}, exclude_unset=True)

    # Handle relationships manually
    company_data['parent'] = parent_company
    company_data['in_charge'] = in_charge_user
    company_data['is_group'] = payload.is_group

    # If it's a group, company_type is None
    if payload.is_group:
        company_data['company_type'] = None

    # Create
    company = Company.objects.create(**company_data)

    print(f"Service: Company created, ID: {company.id}")

    return company

def get_list_companies(
    *,
    search: Optional[str] = None,
    company_type: Optional[str] = None,
    is_group: Optional[bool] = None,
    order_by: str = 'name'
) -> QuerySet[Company]:
    queryset = Company.objects.all()

    if search:
        queryset = queryset.filter(Q(name__icontains=search) | Q(inn__icontains=search) | Q(formal_name__icontains=search))
    if company_type:
        queryset = queryset.filter(company_type=company_type)
    if is_group is not None:
        queryset = queryset.filter(is_group=is_group)

    queryset = queryset.select_related('parent', 'in_charge').prefetch_related(
        'bank_accounts', 'contacts', 'agreements', 'agents'
    )

    if order_by:
        allowed_ordering_fields = {'id', 'name', 'company_type', 'is_group', 'created_at', 'updated_at'}
        validated_fields = validate_ordering_string(order_by, allowed_ordering_fields)
        if validated_fields:
            queryset = queryset.order_by(*validated_fields)
        else:
            queryset = queryset.order_by('name')
    else:
        queryset = queryset.order_by('name')

    return queryset

def validate_ordering_string(ordering_string: str, allowed_fields: set) -> list:
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

        if field_name in allowed_fields:
            validated_fields.append(direction + field_name)
        else:
            logger.warning(f"Ignored invalid sort field: '{field_name}'")

    return validated_fields

# --- Generic CRUD Service Helpers ---

def create_related_object(model_class: Type[models.Model], payload: Schema, company_field_name: str = 'company') -> models.Model:
    data = payload.dict()
    company_id = data.pop(f'{company_field_name}_id')
    company = get_object_or_404(Company, id=company_id)

    obj = model_class.objects.create(**data, **{company_field_name: company})
    return obj

def update_related_object(model_class: Type[models.Model], object_id: int, payload: Schema) -> models.Model:
    obj = get_object_or_404(model_class, id=object_id)
    for attr, value in payload.dict(exclude_unset=True).items():
        if attr == 'company': # Handle company FK update if passed (usually by ID)
            if value:
                obj.company = get_object_or_404(Company, id=value)
        else:
            setattr(obj, attr, value)
    obj.save()
    return obj

# --- Agreement Services ---

def create_agreement(payload: AgreementInputSchema) -> Agreement:
    return create_related_object(Agreement, payload)

def update_agreement(agreement_id: int, payload: AgreementUpdateSchema) -> Agreement:
    return update_related_object(Agreement, agreement_id, payload)

# --- Agent Services ---

def create_agent(payload: AgentInputSchema) -> Agent:
    return create_related_object(Agent, payload)

def update_agent(agent_id: int, payload: AgentUpdateSchema) -> Agent:
    return update_related_object(Agent, agent_id, payload)

# --- BankAccount Services ---

def create_bank_account(payload: BankAccountInputSchema) -> BankAccount:
    return create_related_object(BankAccount, payload)

def update_bank_account(account_id: int, payload: BankAccountUpdateSchema) -> BankAccount:
    return update_related_object(BankAccount, account_id, payload)

from enum import Enum
from typing import Annotated, Literal, Optional, Union, List
from ninja import Schema, ModelSchema
from pydantic import Field
from .models import Company, Business, Agreement, Agent, BankAccount
from contacts.models import Contact

# --- Input Schemas ---

class CompanyBaseInputSchema(Schema):
    name: str = Field(...)
    is_group: Optional[bool] = Field(False)
    parent: Optional[int] = Field(None)
    in_charge_id: Optional[int] = Field(None)

    # New fields
    address: Optional[str] = Field(None)
    mail_address: Optional[str] = Field(None)
    comment: Optional[str] = Field(None)

    # Common fields (previously in info schemas)
    formal_name: Optional[str] = Field(None)

class LegalCompanyInputSchema(CompanyBaseInputSchema):
    company_type: Literal[Business.Types.Legal] = Field(Business.Types.Legal)
    inn: Optional[str] = Field(None)
    kpp: Optional[str] = Field(None)
    ogrn: Optional[str] = Field(None)

class IndividualCompanyInputSchema(CompanyBaseInputSchema):
    company_type: Literal[Business.Types.Individual] = Field(Business.Types.Individual)
    inn: Optional[str] = Field(None)
    ogrn: Optional[str] = Field(None)

class PersonCompanyInputSchema(CompanyBaseInputSchema):
    company_type: Literal[Business.Types.Person] = Field(Business.Types.Person)
    personal_id: Optional[str] = Field(None)

class GroupCompanyInputSchema(CompanyBaseInputSchema):
    is_group: Literal[True] = Field(True)
    company_type: Literal[None] = Field(None)

# Union Schema
CompanyInputUnion = Annotated[
    Union[GroupCompanyInputSchema, LegalCompanyInputSchema, IndividualCompanyInputSchema, PersonCompanyInputSchema],
    Field(discriminator='company_type')
]

# --- Related Models Input/Update Schemas ---

class AgreementInputSchema(ModelSchema):
    company_id: int
    class Meta:
        model = Agreement
        fields = ['number', 'date']

class AgreementUpdateSchema(ModelSchema):
    class Meta:
        model = Agreement
        fields = ['number', 'date', 'company']
        fields_optional = ['number', 'date', 'company']

class AgentInputSchema(ModelSchema):
    company_id: int
    class Meta:
        model = Agent
        fields = ['name', 'position', 'authority_doc', 'details']

class AgentUpdateSchema(ModelSchema):
    class Meta:
        model = Agent
        fields = ['name', 'position', 'authority_doc', 'details', 'company']
        fields_optional = ['name', 'position', 'authority_doc', 'details', 'company']

class BankAccountInputSchema(ModelSchema):
    company_id: int
    class Meta:
        model = BankAccount
        fields = ['number', 'bank', 'bik', 'cor_number']

class BankAccountUpdateSchema(ModelSchema):
    class Meta:
        model = BankAccount
        fields = ['number', 'bank', 'bik', 'cor_number', 'company']
        fields_optional = ['number', 'bank', 'bik', 'cor_number', 'company']

# --- Nested Output Schemas ---

class AgreementSchema(ModelSchema):
    class Meta:
        model = Agreement
        fields = ['id', 'number', 'date']

class AgentSchema(ModelSchema):
    class Meta:
        model = Agent
        fields = ['id', 'name', 'position', 'authority_doc', 'details']

class BankAccountSchema(ModelSchema):
    class Meta:
        model = BankAccount
        fields = ['id', 'number', 'bank', 'bik', 'cor_number']

class ContactSchema(ModelSchema):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone', 'email', 'comment']

class CompanyDetailsSchema(Schema):
    bank_accounts: List[BankAccountSchema]
    contacts: List[ContactSchema]
    agreements: List[AgreementSchema]
    agents: List[AgentSchema]

# --- Output Schemas ---

class CompanyOutputSchema(ModelSchema):
    class Meta:
        model = Company
        fields = [
            'id',
            'name',
            'is_group', 
            'parent',
            'in_charge',
            'company_type',
            'created_at',
            'updated_at',
            'formal_name',
            'inn',
            'kpp',
            'ogrn',
            'personal_id',
            'address',
            'mail_address',
            'comment',
            'main_agreement',
            'representative',
            'main_bank_account'
        ]

class CompanyFullOutputSchema(CompanyOutputSchema):
    details: CompanyDetailsSchema

class CompanyFilterSchema(Schema):
    search: Optional[str] = None
    company_type: Optional[Business.Types] = None
    is_group: Optional[bool] = None
    order_by: Optional[str] = None

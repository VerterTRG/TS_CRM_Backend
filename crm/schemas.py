from enum import Enum
from typing import Annotated, Literal, Optional, Union, List
from ninja import Schema, ModelSchema
from pydantic import Field
from .models import Company, Business

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
            # We can add resolved fields for related objects if needed,
            # but for now we stick to the main model fields.
            # Relationships like agreements are usually fetched via separate endpoints or nested schemas.
        ]
        
    # No more resolve_info needed as fields are on the model

class CompanyFilterSchema(Schema):
    search: Optional[str] = None
    company_type: Optional[Business.Types] = None
    is_group: Optional[bool] = None
    order_by: Optional[str] = None

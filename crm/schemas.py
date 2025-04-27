from enum import Enum
from typing import Annotated, Literal, Optional, Union
from ninja import Schema, ModelSchema # Импортируем оба
from pydantic import Field, computed_field
# ... другие импорты ...
from .models import Company, Business

# --- Схемы для ИНФОРМАЦИИ (теперь на ModelSchema) ---
class LegalInfoSchema(ModelSchema):
    class Meta:
        model = Business.Legal
        # Указываем поля из LegalEntityProfile, нужные в 'info'
        fields = '__all__' # ['formal_name', 'inn', 'kpp', 'ogrn']
        exclude = ['id', 'company']

class IndividualInfoSchema(ModelSchema):
    class Meta:
        model = Business.Individual
        fields = '__all__' # ['formal_name', 'inn', 'ogrn'] # Поле ogrn из вашей модели
        exclude = ['id', 'company']

class PersonInfoSchema(ModelSchema):
    class Meta:
        model = Business.Person
        fields = '__all__' # ['formal_name', 'personal_id']
        exclude = ['id', 'company']


class CompanyBaseInputSchema(Schema):
    name: str = Field(...)
    is_group: Optional[bool] = Field(False, alias="isGroup")
    parent_id: Optional[int] = Field(None, alias="parentId")
    in_charge_id: Optional[int] = Field(None, alias="inChargeId")

class LegalCompanyInputSchema(CompanyBaseInputSchema):
    company_type: Literal[Business.Types.Legal] = Field(Business.Types.Legal, alias="companyType")
    info: LegalInfoSchema # <-- Теперь использует ModelSchema
class IndividualCompanyInputSchema(CompanyBaseInputSchema):
    company_type: Literal[Business.Types.Individual] = Field(Business.Types.Individual, alias="companyType")
    info: IndividualInfoSchema # <-- Теперь использует ModelSchema
class PersonCompanyInputSchema(CompanyBaseInputSchema):
    company_type: Literal[Business.Types.Person] = Field(Business.Types.Person, alias="companyType")
    info: PersonInfoSchema # <-- Теперь использует ModelSchema

class GroupCompanyInputSchema(CompanyBaseInputSchema):
    is_group: Literal[True] = Field(True, alias="isGroup")
    company_type: Literal[None] = Field(None, alias="companyType")
    info: Optional[None] = Field(None)


# --- Объединенная схема ---
CompanyInputUnion = Annotated[
    Union[GroupCompanyInputSchema, LegalCompanyInputSchema, IndividualCompanyInputSchema, PersonCompanyInputSchema],
    Field(discriminator='company_type') # или 'companyType', если использовали alias
]

# CompanyInputUnion = Union[GroupCompanyInputSchema, LegalCompanyInputSchema, IndividualCompanyInputSchema, PersonCompanyInputSchema]

ProfileOutputUnion = Union[LegalInfoSchema, IndividualInfoSchema, PersonInfoSchema, None]
# --- Схема для ОТВЕТА (здесь ModelSchema идеальна) ---
class CompanyOutputSchema(ModelSchema):

    class Meta:
        model = Company
        # Указываем основные поля модели Company.
        fields = [
            'id',
            'name',
            'is_group', 
            'parent',
            'in_charge',
            'company_type',
            'created_at',
            'updated_at',
        ]
    
    # 1. Объявляем поле 'info', которое мы хотим видеть в выводе.
    info: Optional[dict] = Field(None)
        
    
    # 2. Определяем метод разрешения для поля 'info'.
    #    Имя метода должно быть 'resolve_' + имя_поля (resolve_info).
    #    Он принимает 'self' (экземпляр схемы) и 'obj' (экземпляр модели Company).
    @staticmethod
    def resolve_info(obj: Company) -> Optional[dict]: # Возвращает dict
        profile_instance = obj.info
        # ... (Ваша логика if/elif/else) ...
        if isinstance(profile_instance, Business.Legal):
            return LegalInfoSchema.from_orm(profile_instance).model_dump(exclude_unset=True) # Возвращаем dict
        elif isinstance(profile_instance, Business.Individual):
             return IndividualInfoSchema.from_orm(profile_instance).model_dump(exclude_unset=True) # Возвращаем dict
        elif isinstance(profile_instance, Business.Person):
             return PersonInfoSchema.from_orm(profile_instance).model_dump(exclude_unset=True) # Возвращаем dict
        else:
             return None

# Схема для параметров фильтрации (опционально, но хорошо для валидации/Swagger)
class CompanyFilterSchema(Schema):
    search: Optional[str] = None
    # company_type: Optional[str] = None # Можно использовать Literal или Enum, если типы известны
    company_type: Optional[Business.Types] = None
    is_group: Optional[bool] = None
    order_by: Optional[str] = None # Для сортировки
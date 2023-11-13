from django.db import transaction
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
    pass

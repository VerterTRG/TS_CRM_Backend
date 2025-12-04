from django.contrib import admin
from crm.models.companies import Company
from crm.models.common_business_entities import Business

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_type', 'display_name', 'created_at')
    search_fields = ('name', 'formal_name')
    list_filter = ('company_type', 'is_group')
    # Используем inline или ссылки для профилей (Legal, Individual, etc.) если нужно,
    # но пока просто регистрируем основные модели.

@admin.register(Business.Legal)
class LegalAdmin(admin.ModelAdmin):
    list_display = ('formal_name', 'inn', 'kpp', 'ogrn', 'company')
    search_fields = ('formal_name', 'inn')
    autocomplete_fields = ['company']

@admin.register(Business.Individual)
class IndividualAdmin(admin.ModelAdmin):
    list_display = ('formal_name', 'inn', 'ogrn', 'company')
    search_fields = ('formal_name', 'inn')
    autocomplete_fields = ['company']

@admin.register(Business.Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('formal_name', 'personal_id', 'company')
    search_fields = ('formal_name',)
    autocomplete_fields = ['company']

from django.contrib import admin
from crm.models.companies import Company
from crm.models.agreements import Agreement
from crm.models.agents import Agent
from crm.models.bank_accounts import BankAccount

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_type', 'formal_name', 'inn', 'created_at')
    search_fields = ('name', 'formal_name', 'inn')
    list_filter = ('company_type', 'is_group')
    fieldsets = (
        (None, {
            'fields': ('name', 'is_group', 'parent', 'in_charge', 'company_type')
        }),
        ('Details', {
            'fields': ('formal_name', 'inn', 'kpp', 'ogrn', 'personal_id', 'address', 'mail_address', 'comment')
        }),
        ('Relationships', {
            'fields': ('main_agreement', 'representative', 'main_bank_account')
        })
    )

@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'company')
    search_fields = ('number', 'company__name')

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'company')
    search_fields = ('name', 'company__name')

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('number', 'bank', 'company')
    search_fields = ('number', 'company__name')

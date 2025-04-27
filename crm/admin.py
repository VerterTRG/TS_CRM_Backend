from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from crm.models.common_business_entities import Business

from crm.models.copmanies import Company

class LegalInline(admin.StackedInline):
    model = Business.Legal
    can_delete = False
    verbose_name_plural = 'legal'

class IndividualInline(admin.StackedInline):
    model = Business.Individual
    can_delete = False
    verbose_name_plural = 'individual'

class PersonInline(admin.StackedInline):
    model = Business.Person
    can_delete = False
    verbose_name_plural = 'person'

class CompanyAdmin(admin.ModelAdmin):
    fields = ['name', 'is_group', 'parent', 'in_charge', 'typeOfBusiness',]
    inlines = [
        LegalInline,
        IndividualInline,
        PersonInline,
    ]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # Для новых объектов показываем все inline формы
            if obj is None:
                yield inline.get_formset(request, obj), inline
                continue
            # Для существующих объектов показываем только те inline формы, для которых есть связанные данные
            if isinstance(inline, LegalInline) and hasattr(obj, 'legal'):
                yield inline.get_formset(request, obj), inline
            elif isinstance(inline, IndividualInline) and hasattr(obj, 'individual'):
                yield inline.get_formset(request, obj), inline
            elif isinstance(inline, PersonInline) and hasattr(obj, 'person'):
                yield inline.get_formset(request, obj), inline
    
    class Meta:
        model = Company

admin.site.register(Company, CompanyAdmin)
admin.site.register(Business.Legal)
admin.site.register(Business.Individual)
admin.site.register(Business.Person)

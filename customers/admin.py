from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from customers.models import Client, Domain

@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'paid_until', 'on_trial', 'created_on')

    def has_module_permission(self, request):
        # Only superusers can see this module
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(Domain)
class DomainAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('domain', 'tenant')

    def has_module_permission(self, request):
        return request.user.is_superuser

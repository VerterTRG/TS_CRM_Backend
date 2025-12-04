from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Fieldsets to include new fields
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'logo')}),
        (_('Tenant Info'), {'fields': ('client',)}), # New section
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'client', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'client')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'client__name')
    ordering = ('username',)

    def get_queryset(self, request):
        """
        Filter queryset based on user role.
        Superuser sees all.
        Staff sees only users from their client.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        # If user has a client, filter by it.
        # If user has no client (but is staff), they probably shouldn't see anything or just themselves.
        # Assuming staff always has a client.
        if request.user.client:
            return qs.filter(client=request.user.client)

        # Fallback for staff without client (should technically not happen in valid setup)
        return qs.none()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # If not superuser, disable 'client' field
        if not request.user.is_superuser:
            if 'client' in form.base_fields:
                form.base_fields['client'].disabled = True
                # Or exclude it entirely if preferred:
                # del form.base_fields['client']
        return form

    def save_model(self, request, obj, form, change):
        # If not superuser, ensure the new user belongs to the same client
        if not request.user.is_superuser:
            if not obj.pk: # Creating new user
                obj.client = request.user.client
            # If editing, 'client' is disabled so it shouldn't change,
            # but we can enforce it here just in case.
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        # Allow superusers and staff to add users
        return request.user.is_superuser or request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

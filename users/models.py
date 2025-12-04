from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from typing import Optional
from customers.models import Client

class CustomUser(AbstractUser):
    """
    Custom user model for the SaaS application.
    Stores user details and links to a specific Client (Tenant).
    """

    # Standard fields from AbstractUser:
    # username, first_name, last_name, email, password, is_staff, is_active, date_joined

    # Overriding/Adding fields with explicit verbose_name and requirements
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    phone = models.CharField(_("Phone"), max_length=20, blank=True, null=True)
    logo = models.ImageField(_("Logo"), upload_to='user_logos/', blank=True, null=True)

    # Client (Tenant) link
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Client (Company)"),
        related_name="users"
    )

    # Use email as the main identifier if desired, but prompt implied 'username' is still used as a field.
    # However, usually in SaaS email is better.
    # The prompt says: "have fields... username (User Name)..." so I will keep username.
    
    class Meta:
        db_table = 'users'
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} ({self.username})"
        return self.username

    @property
    def client_name(self) -> Optional[str]:
        """Returns the name of the associated client."""
        if self.client:
            return self.client.name
        return None

    @property
    def schema_name(self) -> Optional[str]:
        """Returns the schema name of the associated client."""
        if self.client:
            return self.client.schema_name
        return None

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from typing import Optional
from customers.models import Client

class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя для SaaS приложения.
    Хранит данные пользователя и ссылку на конкретного Клиента (Тенанта).
    """

    # Стандартные поля от AbstractUser:
    # username, first_name, last_name, email, password, is_staff, is_active, date_joined

    # Переопределение полей для явного указания verbose_name на русском языке
    # Удаляем первый позиционный аргумент (который является verbose_name по умолчанию),
    # так как мы передаем его явно через verbose_name=...

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        verbose_name="Имя пользователя"
    )
    first_name = models.CharField(max_length=150, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="Фамилия")
    
    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
        verbose_name="Эл. почта"
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    logo = models.ImageField(upload_to='user_logos/', blank=True, null=True, verbose_name="Лого")

    # Ссылка на Клиента (Тенант)
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Компания (Клиент)",
        related_name="users"
    )

    is_staff = models.BooleanField(
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
        verbose_name="Администратор"
    )

    class Meta:
        db_table = 'users'
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} ({self.username})"
        return self.username

    @property
    def client_name(self) -> Optional[str]:
        """Возвращает название связанного клиента."""
        if self.client:
            return self.client.name
        return None

    @property
    def schema_name(self) -> Optional[str]:
        """Возвращает имя схемы связанного клиента."""
        if self.client:
            return self.client.schema_name
        return None

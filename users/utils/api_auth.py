import logging
from typing import Optional, Any
from django.db import connection
from django.http import HttpRequest
from ninja_jwt.authentication import JWTAuth # Наследуем от него
# Импорты ваших моделей
from customers.models import Client
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model() # Ваша CustomUser

class TenantAwareJWTAuth(JWTAuth):
    """
    Кастомный JWT аутентификатор, который устанавливает схему тенанта
    ПОСЛЕ успешной аутентификации по токену.
    """
    def authenticate(self, request: HttpRequest, token: str) -> Optional['User']:  # type: ignore
        # 1. Вызываем стандартную JWT аутентификацию родительского класса
        # Она вернет пользователя, если токен валиден, или None/выбросит исключение
        user = super().authenticate(request, token)

        # 2. Устанавливаем схему ТОЛЬКО если аутентификация прошла успешно
        if user is not None and user.is_authenticated:
            tenant: Optional[Client] = None
            try:
                # Получаем тенанта
                tenant = getattr(user, 'client', None)
                if not isinstance(tenant, Client):
                    if not user.is_superuser:
                        logger.warning(f"(Auth) User {user.pk} has no Client linked.")
                    tenant = None
            except AttributeError:
                logger.error(f"(Auth) CustomUser model missing 'client' attribute.")
                tenant = None

            # Устанавливаем схему
            if tenant:
                connection.set_tenant(tenant)
                logger.info(f"(Auth) Set schema to {tenant.schema_name} for user {user}")
            else:
                # Если у аутентифицированного пользователя нет тенанта (напр., superuser)
                connection.set_schema_to_public()
                logger.info(f"(Auth) Using public schema for authenticated user {user}")
        else:
            # Если аутентификация не прошла, остаемся в public схеме
            connection.set_schema_to_public()
            logger.info(f"(Auth) JWT Auth failed or user inactive, using public schema.")

        # 3. Возвращаем результат аутентификации (пользователя или None)
        return user
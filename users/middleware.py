from django.db import connection
from django.http import HttpRequest, HttpResponse
from django.utils.functional import SimpleLazyObject # Рекомендуется для request.user
from typing import Callable, Optional

# Импортируем ВАШУ модель тенанта
from customers.models import Client

# Импортируем модель пользователя ДИНАМИЧЕСКИ через get_user_model()
# Это лучшая практика, Django сам найдет вашу CustomUser
from django.contrib.auth import get_user_model

User = get_user_model() # User теперь ссылается на вашу CustomUser

class TenantIdentificationMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Определяет тенанта (Client) на основе залогиненного пользователя (CustomUser).
        """
        # 1. Устанавливаем public схему по умолчанию. Важно для логина и shared моделей.
        connection.set_schema_to_public()
        tenant: Optional[Client] = None # Используем Optional и вашу модель Client

        # 2. Получаем пользователя безопасно через SimpleLazyObject
        # Это позволяет избежать лишнего обращения к request.user, если он не нужен
        user_lazy = SimpleLazyObject(lambda: getattr(request, 'user', None))

        # 3. Проверяем, аутентифицирован ли пользователь
        if user_lazy and user_lazy.is_authenticated:
            # Получаем реальный объект пользователя (ваша CustomUser)
            user: User = user_lazy # type: ignore
            try:
                # 4. Получаем тенанта (Client) через поле связи в CustomUser
                tenant_from_user = getattr(user, 'client', None)

                # 5. Проверяем, что получили действительно объект Client (а не None)
                if isinstance(tenant_from_user, Client):
                    tenant = tenant_from_user
                else:
                    # Пользователь аутентифицирован, но не привязан к Client
                    # Это может быть нормально для суперпользователя
                    # Или ошибка конфигурации для обычного пользователя
                    if not user.is_superuser:
                        # Здесь нужна ваша логика: записать в лог, показать ошибку?
                        # print(f"Warning: User {user.pk} ({user.email}) has no Client linked.") # Замените на logging
                        pass # Оставляем tenant = None, пользователь останется в public схеме
                    # Если это суперпользователь без клиента, он останется в public схеме

            except AttributeError:
                # Ошибка: У вашей модели CustomUser нет атрибута/поля 'client'
                # Проверьте определение модели users.models.CustomUser
                # print(f"Error: CustomUser model missing 'client' attribute.") # Замените на logging
                pass # Оставляем tenant = None

        # 6. Устанавливаем схему тенанта, если он был найден
        if tenant:
            connection.set_tenant(tenant)
            # Опционально: сохраняем тенанта в запросе для удобства
            # Добавлена опциональная строка request.tenant = tenant (или request.client = tenant), 
            # которая позволяет легко получить доступ к текущему объекту тенанта в ваших views, 
            # если это нужно.
            # request.tenant = tenant # Или request.client = tenant, как вам удобнее
            # print(f"Activated schema for tenant: {tenant.schema_name}") # Для отладки
        else:
            # Если тенант не найден, оставляем public схему (уже установлена)
            # request.tenant = None
            pass
            # print("Using public schema") # Для отладки


        # 7. Передаем управление дальше
        response = self.get_response(request)

        # Код здесь выполнится после view, перед отправкой ответа клиенту

        return response

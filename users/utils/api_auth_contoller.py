from ninja_extra import api_controller
from ninja_jwt.controller import NinjaJWTDefaultController

@api_controller("/auth/token", tags=["Authentication"], auth=None) # Префикс /auth, можно добавить тег, auth=None т.к. для логина/рефреша обычно аутентификация не нужна
class AuthController(NinjaJWTDefaultController): # type: ignore
    # Этот класс наследует все эндпоинты (/token/obtain, /token/refresh, /token/verify)
    # из NinjaJWTDefaultController, но теперь они все будут автоматически
    # доступны с префиксом /auth (т.е. /auth/token/obtain и т.д.)
    # Можно переопределить или добавить свои методы, если нужно.
    pass
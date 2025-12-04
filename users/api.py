from typing import Optional
from ninja import Router, File, UploadedFile, Form
from ninja.errors import HttpError
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from ninja_extra import api_controller, http_get, http_put, http_post
from ninja_jwt.authentication import JWTAuth
from users.schemas import UserOut, UserUpdate, PasswordChange

User = get_user_model()

@api_controller('/users', tags=['Пользователи'], auth=JWTAuth())
class UserController:
    @http_get("/me", response=UserOut, summary="Получить профиль текущего пользователя")
    def get_me(self, request):
        """
        Возвращает профиль текущего авторизованного пользователя.
        Включает информацию о компании (тенанте), если она доступна.
        """
        return request.user

    @http_put("/me", response=UserOut, summary="Обновить профиль пользователя")
    def update_me(self, request, payload: UserUpdate):
        """
        Обновляет информацию профиля текущего пользователя.
        Принимает стандартный JSON.
        """
        user = request.user

        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(user, attr, value)

        user.save()
        return user

    @http_post("/me/logo-upload", response=UserOut, summary="Обновить аватар")
    def upload_avatar(self, request, logo: UploadedFile = File(...)): #type: ignore
        """
        Отдельный эндпоинт для загрузки аватара (multipart/form-data).
        """
        user = request.user
        # save=True сохранит файл и обновит модель
        user.logo.save(logo.name, logo, save=True)
        return user

    @http_post("/change-password", summary="Сменить пароль")
    def change_password(self, request, payload: PasswordChange):
        """
        Меняет пароль пользователя. Требует подтверждения старого пароля.
        """
        user = request.user
        if not user.check_password(payload.old_password):
            raise HttpError(400, "Старый пароль неверен")

        if payload.new_password != payload.new_password_confirm:
            raise HttpError(400, "Новые пароли не совпадают")

        user.set_password(payload.new_password)
        user.save()
        update_session_auth_hash(request, user) # Сохраняет пользователя авторизованным
        return {"message": "Пароль успешно обновлен"}

from typing import Optional
from ninja import Router, File, UploadedFile, Form
from ninja.errors import HttpError
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from ninja_extra import api_controller, http_get, http_put, http_post
from ninja_jwt.authentication import JWTAuth
from users.schemas import UserOut, UserUpdate, PasswordChange

User = get_user_model()

@api_controller('/users', tags=['Users'], auth=JWTAuth())
class UserController:
    @http_get("/me", response=UserOut, summary="Get current user profile")
    def get_me(self, request):
        """
        Returns the profile of the currently logged-in user.
        Includes client (tenant) information if available.
        """
        return request.user

    @http_put("/me", response=UserOut, summary="Update user profile")
    def update_me(self, request, payload: UserUpdate = Form(...), logo: UploadedFile = File(None)):
        """
        Updates the current user's profile information.
        """
        user = request.user

        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(user, attr, value)

        if logo:
            user.logo.save(logo.name, logo, save=False)

        user.save()
        return user

    @http_post("/change-password", summary="Change password")
    def change_password(self, request, payload: PasswordChange):
        """
        Changes the user's password. Requires old password verification.
        """
        user = request.user
        if not user.check_password(payload.old_password):
            raise HttpError(400, "Old password is not correct")

        if payload.new_password != payload.new_password_confirm:
            raise HttpError(400, "New passwords do not match")

        user.set_password(payload.new_password)
        user.save()
        update_session_auth_hash(request, user) # Keeps the user logged in
        return {"message": "Password updated successfully"}

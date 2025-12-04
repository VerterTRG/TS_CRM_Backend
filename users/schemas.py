from ninja import Schema, UploadedFile
from typing import Optional

class ClientSchema(Schema):
    name: str
    schema_name: str

class UserOut(Schema):
    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    phone: Optional[str] = None
    logo: Optional[str] = None
    client: Optional[ClientSchema] = None
    is_staff: bool
    is_active: bool

class UserUpdate(Schema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    # Logo is handled via file upload separately usually, but can be base64 or multipart

class PasswordChange(Schema):
    old_password: str
    new_password: str
    new_password_confirm: str

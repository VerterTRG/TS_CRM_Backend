from typing import Optional
from ninja import Router, Schema
from drf_spectacular.utils import extend_schema



router = Router()

class UserSchema(Schema):
    username: str
    is_authenticated: bool
    client_name: str = None # type: ignore You can use Optional[str]
    schema_name: Optional[str] = None



 # Простой extend_schema
# @api.get("/me", response=UserSchema, auth=JWTAuth())
@router.get("/me", response=UserSchema)
# @extend_schema(summary="Простой тестовый эндпоинт CRM")
def hello(request):
    print(request)
    return request.user

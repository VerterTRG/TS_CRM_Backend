
from typing import Annotated, Optional
from contacts.models import Contact
from ninja import NinjaAPI, ModelSchema, Schema, Redoc, Form, Query
from ninja.orm import create_schema


# api = NinjaAPI(docs=Redoc())
api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "Hello world"

# class ContactSchema(Schema):
#     name: str
#     phone: str = None
#     email: str = None

# class ContactSchema(ModelSchema):
#     class Meta:
#         model = Contact
#         fields = "__all__"

ContactSchema = create_schema(Contact)


@api.post("/new")
async def create_contact(request, data: Annotated[ContactSchema, Query()]):
    
    contact = await Contact.objects.acreate(**data.dict())

    return f'Contact has been created. Id:{contact.id}'

class STaskAdd(Schema):
    name: str
    description: Optional[str] = None

class STask(STaskAdd):
    id: int

@api.post('/task')
async def add_task(task: Annotated[STaskAdd, Query()]):
    return {'ok': 200}
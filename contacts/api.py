
from typing import Annotated, Optional, List
from contacts.models import Contact
from ninja import Router, Schema, Redoc, Swagger
from ninja.orm import create_schema


router = Router()

@router.get("/hello")
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

@router.get("/list", response=List[ContactSchema])
async def get_contact_list(request):
    # Асинхронно итерируем queryset и собираем объекты в список
    contacts_list = [contact async for contact in Contact.objects.all()] 
    
    # Возвращаем готовый список объектов Python
    return contacts_list



@router.post("/new")
async def create_contact(request, data: ContactSchema): # type: ignore
    
    contact = await Contact.objects.acreate(**data.dict())

    return f'Contact has been created. Id:{contact.id}' # type: ignore

class STaskAdd(Schema):
    name: str
    description: Optional[str] = None

class STask(STaskAdd):
    id: int

@router.post('/task')
async def add_task(request, task: STaskAdd):
    print(task.name, task.description)
    return {'ok': 200}
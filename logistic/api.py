from typing import Annotated, Optional, List
from logistic.models import Driver, Truck, Assignment
from ninja import Router, Schema, Redoc, Swagger
from ninja.orm import create_schema
from ninja_extra import api_controller

from logistic.schemas import DriverInputSchema, TruckInputSchema, AssignmentInputSchema, DriverOutputSchema, TruckOutputSchema, AssignmentOutputSchema
from .services import create_driver, create_truck, create_assignment

router = Router()

class ErrorSchema(Schema):
    detail: str
    field_errors: Optional[dict] = None


@api_controller("logistic", tags=["Logistic"])
class LogisticController:

    @router.get("/hello", auth=None)
    def simple_logistic_test(self, request):
        """Просто возвращает приветствие из Logistic."""
        return {"message": "Hello from Logistic API!"}
    

    @router.get(
            "/driver/list", 
            tags=["Drivers"],
            summary="Возвращает список всех водителей",
            response={
                200: List[DriverOutputSchema],
                500: ErrorSchema
            }
    )
    def get_driver_list(self, request):
        """Возвращает список всех водителей."""
        drivers_list = Driver.objects.all()
        return drivers_list
    
    @router.post(
            "/driver/create", 
            tags=["Drivers"],
            summary="Создает нового водителя",
            response={
                200: DriverInputSchema,
                500: ErrorSchema
            }
    )
    def create_driver(self, request, payload: DriverInputSchema):
        """Создает нового водителя."""

        print(f"API: Получен запрос на создание {request.body.decode('utf-8')}")
        driver = create_driver(payload)
        return driver
    

    @router.get(
            "/truck/list", 
            tags=["Trucks"],
            summary="Возвращает список всех грузовиков",
            response={
                200: List[TruckOutputSchema],
                500: ErrorSchema
            }
    )
    def get_truck_list(self, request):
        """Возвращает список всех грузовиков."""
        trucks_list = Truck.objects.all()
        return trucks_list
    
    @router.post(
            "/truck/create",
            tags=["Trucks"],
            summary="Создает новый грузовик",
            response={
                200: TruckInputSchema,
                500: ErrorSchema
            }
    )
    def create_truck(self, request, payload: TruckInputSchema):
        """Создает новый грузовик."""
        print(f"API: Получен запрос на создание {request.body.decode('utf-8')}")
        truck = create_truck(payload)
        return truck


    @router.get(
            "/assignment/list",
            tags=["Assignments"],
            summary="Возвращает список всех заявок",
            response={
                200: List[AssignmentOutputSchema],
                500: ErrorSchema
            }
    )
    def get_assignment_list(self, request):
        """Возвращает список всех заявок."""
        assignments_list = Assignment.objects.all()
        return assignments_list
    
    @router.post(
            "/assignment/create",
            tags=["Assignments"],
            summary="Создает новую заявку",
            response={
                200: AssignmentInputSchema,
                500: ErrorSchema
            }
    )
    def create_assignment(self, request, payload: AssignmentInputSchema):
        """Создает новую заявку."""
        print(f"API: Получен запрос на создание {request.body.decode('utf-8')}")
        assignment = create_assignment(payload)
        return assignment



# DriverSchema = create_schema(Driver)
# TruckSchema = create_schema(Truck)
# AssignmentSchema = create_schema(Assignment)

# @router.get("/drivers", response=List[DriverSchema])
# async def get_driver_list(request):
#     drivers_list = [driver async for driver in Driver.objects.all()] 
#     return drivers_list

# @router.post("/new_driver")
# async def create_driver(request, data: DriverSchema):
#     driver = await Driver.objects.acreate(**data.dict())
#     return f'Driver has been created. Id:{driver.id}'

# @router.get("/trucks", response=List[TruckSchema])
# async def get_truck_list(request):
#     trucks_list = [truck async for truck in Truck.objects.all()] 
#     return trucks_list

# @router.post("/new_truck")
# async def create_truck(request, data: TruckSchema):
#     truck = await Truck.objects.acreate(**data.dict())
#     return f'Truck has been created. Id:{truck.id}'

# @router.get("/assignments", response=List[AssignmentSchema])
# async def get_assignment_list(request):
#     assignments_list = [assignment async for assignment in Assignment.objects.all()] 
#     return assignments_list

# @router.post("/new_assignment")
# async def create_assignment(request, data: AssignmentSchema):
#     assignment = await Assignment.objects.acreate(**data.dict())
#     return f'Assignment has been created. Id:{assignment.id}'
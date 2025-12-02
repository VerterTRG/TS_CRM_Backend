from typing import Annotated, Literal, Optional, Union
from ninja import Schema, ModelSchema # Импортируем оба
from pydantic import Field
from .models import Driver, Truck, Assignment


class DriverOutputSchema(ModelSchema):
    class Meta:
        model = Driver
        fields = '__all__'

class TruckOutputSchema(ModelSchema):
    class Meta:
        model = Truck
        fields = '__all__'

class AssignmentOutputSchema(ModelSchema):
    class Meta:
        model = Assignment
        fields = '__all__'

class DriverInputSchema(Schema):
    name: str = Field(...)
    license_number: str = Field(...)
    phone_number: Optional[str] = Field(None)

class TruckInputSchema(Schema):
    license_plate: str = Field(...)
    model: str = Field(...)
    capacity_tons: float = Field(...)

class AssignmentInputSchema(Schema):
    driver_id: int = Field(...)
    truck_id: int = Field(...)
    assignment_date: str = Field(...)
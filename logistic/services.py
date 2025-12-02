from django.db.models import QuerySet, Q
from multiprocessing.managers import BaseManager
from django.db import transaction
from django.contrib.auth import get_user_model
from typing import Optional, Union
from ninja.errors import HttpError

import logging # <-- Или используем logging вместо print

logger = logging.getLogger(__name__) # Настраиваем логгер


from .models import Driver, Truck, Assignment
from .schemas import DriverInputSchema, TruckInputSchema, AssignmentInputSchema

User = get_user_model()

@transaction.atomic
def create_driver(data: DriverInputSchema) -> Driver:
    """
    Сервисная функция для создания нового водителя.
    Выполняется в атомарной транзакции.
    """
    print(f"Сервис: Запрос на создание водителя с данными {data.dict()}")
    driver = Driver.objects.create(**data.dict())
    return driver


@transaction.atomic
def create_truck(data: TruckInputSchema) -> Truck:
    """
    Сервисная функция для создания нового грузовика.
    Выполняется в атомарной транзакции.
    """
    print(f"Сервис: Запрос на создание грузовика с данными {data.dict()}")
    truck = Truck.objects.create(**data.dict())
    return truck


@transaction.atomic
def create_assignment(data: AssignmentInputSchema) -> Assignment:
    """
    Сервисная функция для создания нового назначения.
    Выполняется в атомарной транзакции.
    """
    print(f"Сервис: Запрос на создание назначения с данными {data.dict()}")
    assignment = Assignment.objects.create(**data.dict())
    return assignment
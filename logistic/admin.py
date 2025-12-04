from django.contrib import admin
from logistic.models.drivers import Driver
from logistic.models.trucks import Truck
from logistic.models.assignments import Assignment
from logistic.models.dispatch import Dispatch

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'type_id', 'driver_licence')
    search_fields = ('name', 'phone', 'driver_licence')

@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ('brand', 'registration', 'type_truck')
    search_fields = ('brand', 'registration')
    list_filter = ('type_truck',)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_open', 'driver', 'truck', 'is_open')
    list_filter = ('is_open', 'date_open')
    search_fields = ('driver__name', 'truck__registration')
    autocomplete_fields = ['driver', 'truck']

@admin.register(Dispatch)
class DispatchAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'route', 'rate', 'payment', 'dateBegin', 'dateEnds')
    search_fields = ('number', 'route', 'contact_tmp')
    list_filter = ('payment', 'date')

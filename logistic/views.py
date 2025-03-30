from rest_framework import viewsets, permissions

from .serializers import *

class DriverViewSet(viewsets.ModelViewSet):
    serializer_class = DriverSerializer
    queryset = Driver.objects.all()

    permission_classes = [permissions.IsAuthenticated]

class TruckViewSet(viewsets.ModelViewSet):
    serializer_class = TruckSerializer
    queryset = Truck.objects.all()

class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()

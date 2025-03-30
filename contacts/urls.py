from django.urls import path
from .api import api

urlpatterns = [
    # ... другие URL-конфигурации ...
    path('', api.urls),
 
]
from django.urls import path
from .views import CompanyCreateView

urlpatterns = [
    # ... другие URL-конфигурации ...
    path('company/add/', CompanyCreateView.as_view(), name='add-company'),
    # ... другие URL-конфигурации ...
]
from django.urls import path
from .views import CompanyCreateView, CompanyListView

urlpatterns = [
    # ... другие URL-конфигурации ...
    path('', CompanyListView.as_view(), name='list-company'),
    # path('<int:parent>', CompanyListView.as_view(), name='list-company'),
    path('company/<int:pk>', CompanyListView.as_view(), name='detail-company'),
    path('company/add/', CompanyCreateView.as_view(), name='add-company'),
    # ... другие URL-конфигурации ...
]
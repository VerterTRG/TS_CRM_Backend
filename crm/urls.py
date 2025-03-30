from django.urls import path
from .views import Home, CompanyCreateView, CompanyListView, CompanyDetail

urlpatterns = [
    # ... другие URL-конфигурации ...
    path('', Home.as_view(), name='Home'),
    path('company/', CompanyListView.as_view(), name='list-company'),
    # path('<int:parent>', CompanyListView.as_view(), name='list-company'),
    path('company/<int:pk>', CompanyDetail.as_view(), name='detail-company'),
    path('company/add/', CompanyCreateView.as_view(), name='add-company'),
    # ... другие URL-конфигурации ...
]
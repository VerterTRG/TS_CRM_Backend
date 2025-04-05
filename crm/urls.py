from django.urls import path
# from .views import Home, CompanyCreateView, CompanyListView, CompanyDetail
from .views import CompanyListView, CompanyDetailView, CompanyCreateView, CompanyUpdateView, CompanyDeleteView  

urlpatterns = [
    # ... другие URL-конфигурации ...
    # path('', Home.as_view(), name='Home'),
    # path('company/', CompanyListView.as_view(), name='list-company'),
    # # path('<int:parent>', CompanyListView.as_view(), name='list-company'),
    # path('company/<int:pk>', CompanyDetail.as_view(), name='detail-company'),
    # path('company/add/', CompanyCreateView.as_view(), name='add-company'),
    # ... другие URL-конфигурации ...
    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('company/create/', CompanyCreateView.as_view(), name='company-create'),
    path('company/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('company/<int:pk>/update/', CompanyUpdateView.as_view(), name='company-update'),
    path('company/<int:pk>/delete/', CompanyDeleteView.as_view(), name='company-delete'),
]
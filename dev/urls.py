
from django.contrib import admin
from django.urls import path, include
from logistic.routers import router as logistic_router
from schema_graph.views import Schema
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Добавляем стандартные URL'ы аутентификации Django
    # Они будут доступны по префиксу /accounts/ (например, /accounts/login/, /accounts/logout/)
    path('accounts/', include('django.contrib.auth.urls')),
    path("schema/", Schema.as_view()),
    path("", include('crm.urls')),
    
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path("api/logistic/", include(logistic_router.urls)),
    path("api/contacts/", include('contacts.urls'))
]

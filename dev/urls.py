
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from ninja import Swagger, NinjaAPI, Redoc
from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from crm.api import CompanyController, AgreementController, AgentController, BankAccountController
from logistic.api import LogisticController
from logistic.routers import router as logistic_router
from schema_graph.views import Schema
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from users.utils.api_auth import TenantAwareJWTAuth
from users.utils.api_auth_contoller import AuthController
from users.api import UserController


api = NinjaExtraAPI(docs=Swagger(), auth=TenantAwareJWTAuth())
api.register_controllers(AuthController)
api.register_controllers(CompanyController)
api.register_controllers(AgreementController)
api.register_controllers(AgentController)
api.register_controllers(BankAccountController)
api.register_controllers(LogisticController)
api.register_controllers(UserController)

api.add_router('/contacts', 'contacts.api.router', tags=["Contacts Simple Test"])
api.add_router('/crm', 'crm.api.router', tags=["CRM Simple Test"])
# api.add_router('/users', 'users.api.router', tags=['Users API']) # Replaced by controller
api.add_router('/logistic', 'logistic.api.router', tags=['Logistic API'])

def redoc_view(request):
    # render_page генерирует HTML для Redoc, используя схему вашего api
    return Redoc().render_page(request, api)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Добавляем стандартные URL'ы аутентификации Django
    # Они будут доступны по префиксу /accounts/ (например, /accounts/login/, /accounts/logout/)
    path('accounts/', include('django.contrib.auth.urls')),
    path("schema/", Schema.as_view()),
    
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # # Optional UI:
    # path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/', api.urls),
    path("api/redoc/", redoc_view, name='redoc'),

    # path("api/logistic/", include(logistic_router.urls)), # DRF


]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

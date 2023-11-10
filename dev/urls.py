
from django.contrib import admin
from django.urls import path, include
from schema_graph.views import Schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path("schema/", Schema.as_view()),
    path("", include('crm.urls'))
]

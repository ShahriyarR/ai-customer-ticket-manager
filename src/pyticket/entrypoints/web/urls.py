"""URL configuration for Django web entrypoint"""

from django.contrib import admin
from django.urls import path

from pyticket.entrypoints.web.api.router import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

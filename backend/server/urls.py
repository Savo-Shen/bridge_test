from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import Server

router = DefaultRouter()
router.register(r'', Server, 'server')

urlpatterns = [
    path("", include(router.urls))
]
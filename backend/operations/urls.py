from django.urls import include, path
from rest_framework import routers

from .views import OperationsViewSet

router = routers.DefaultRouter()
router.register("operations", OperationsViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

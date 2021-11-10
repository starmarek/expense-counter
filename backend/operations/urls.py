from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, OperationsViewSet

router = routers.DefaultRouter()
router.register("operations", OperationsViewSet)
router.register("category", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

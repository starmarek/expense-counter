from django.urls import include, path
from rest_framework import routers

from .views import validation_view

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("validation-view/", validation_view, name="validation_view"),
]

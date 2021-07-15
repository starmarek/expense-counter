from django.urls import include, path
from rest_framework import routers

from .views import BankStatementViewSet

router = routers.DefaultRouter()
router.register("bank_statement", BankStatementViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

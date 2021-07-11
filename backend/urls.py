"""project URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .api.views import MessageViewSet, index_view
from .bank_statement.views import BankStatementViewSet
from .operations.views import OperationsViewSet
from .user.views import UserViewSet

router = routers.DefaultRouter()
router.register("messages", MessageViewSet)
router.register("operations", OperationsViewSet)
router.register("bank_statement", BankStatementViewSet)
router.register("user", UserViewSet)


urlpatterns = [
    path("", index_view, name="index"),
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
]

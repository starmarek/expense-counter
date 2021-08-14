"""project URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from itertools import chain

from django.contrib import admin
from django.urls import include, path

from .bank_statement.urls import urlpatterns as b_statement_urls
from .operations.urls import urlpatterns as operations_urls
from .user.urls import urlpatterns as user_urls
from .validation.urls import urlpatterns as validation_urls

api_urlpatterns = list(chain.from_iterable([b_statement_urls, operations_urls, user_urls, validation_urls]))
urlpatterns = [
    path("", include("backend.vue_api.urls")),
    path("api/", include(api_urlpatterns)),
    path("admin/", admin.site.urls),
]

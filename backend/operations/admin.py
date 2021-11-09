from django.contrib import admin

from .models import Category, Operations

admin.site.register(Operations)
admin.site.register(Category)

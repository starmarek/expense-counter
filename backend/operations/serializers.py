from rest_framework import serializers

from .models import Category, Operations


class OperationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operations
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

from rest_framework import serializers

from .models import Message, Operations


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ("url", "subject", "body", "pk")


class OperationsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Operations
        fields = ("url", "datetime", "category", "operation_type", "isExpense", "pk")

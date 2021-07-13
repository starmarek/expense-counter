from rest_framework import serializers

from .models import BankStatement


class BankStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankStatement
        fields = "__all__"

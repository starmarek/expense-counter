from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from rest_framework import viewsets

from .models import BankStatement
from .serializers import BankStatementSerializer

index_view = never_cache(TemplateView.as_view(template_name="index.html"))


class BankStatementViewSet(viewsets.ModelViewSet):
    queryset = BankStatement.objects.all()
    serializer_class = BankStatementSerializer

from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from rest_framework import viewsets

from .models import Operations
from .serializers import OperationsSerializer

index_view = never_cache(TemplateView.as_view(template_name="index.html"))


class OperationsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows operations to be viewed or edited
    """

    queryset = Operations.objects.all()
    serializer_class = OperationsSerializer

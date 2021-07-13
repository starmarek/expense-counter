from rest_framework import viewsets

from .models import Operations
from .serializers import OperationsSerializer


class OperationsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows operations to be viewed or edited
    """

    queryset = Operations.objects.all()
    serializer_class = OperationsSerializer

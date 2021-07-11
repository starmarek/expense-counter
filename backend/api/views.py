from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from rest_framework import viewsets

from .models import Message, Operations
from .serializers import MessageSerializer, OperationsSerializer

# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name="index.html"))


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class OperationsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows operations to be viewed or edited
    """

    queryset = Operations.objects.all()
    serializer_class = OperationsSerializer

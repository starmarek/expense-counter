from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, status, viewsets
from rest_framework.response import Response

from .models import Category, Operations
from .serializers import CategorySerializer, OperationsSerializer


class CustomPagination(pagination.PageNumberPagination):
    page_size = 25


class OperationsFilter(filters.FilterSet):
    date = filters.DateFilter(field_name="date")
    value = filters.RangeFilter(field_name="value")
    category = filters.CharFilter(field_name="category", lookup_expr="icontains")
    operation_type = filters.CharFilter(field_name="operation_type", lookup_expr="icontains")

    ordering = filters.OrderingFilter(
        fields=(
            ("id", "id"),
            ("date", "date"),
            ("time", "time"),
            ("value", "value"),
            ("category", "category"),
            ("operation_type", "operation_type"),
            ("balance", "balance"),
        )
    )

    class Meta:
        model = Operations
        fields = ["date", "value", "category", "operation_type"]


class OperationsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows operations to be viewed or edited
    queryset filtration
    """

    queryset = Operations.objects.all().order_by("id")
    pagination_class = CustomPagination
    serializer_class = OperationsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OperationsFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page_param = request.query_params.get("page", None)

        if page_param is not None:
            queryset = self.paginate_queryset(queryset)

        serializer = self.get_serializer(queryset, many=True)

        return self.get_paginated_response(serializer.data) if page_param else Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        detail = instance.details
        category = request.data["category"]
        for instance in Operations.objects.all().filter(details=detail):
            instance.category = Category.objects.get(name=category)
            instance.save()

        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        if request.data["name"] in [ob.name for ob in Category.objects.all()]:
            return Response("Category already created.", status=409)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

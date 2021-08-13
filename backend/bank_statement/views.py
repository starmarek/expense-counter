from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db.utils import IntegrityError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.operations.models import Operations

from .models import BankStatement
from .scraper import getOperations, getStatementDate, getTextPdf
from .serializers import BankStatementSerializer


class BankStatementViewSet(viewsets.ModelViewSet):
    queryset = BankStatement.objects.all()
    serializer_class = BankStatementSerializer

    @action(detail=False, methods=["post"])
    def loader(self, request):
        for name, file in request.FILES.items():
            file_name = default_storage.save("backend/bank_statement/store/" + name, file)
            text_file = getTextPdf(file_name)
            operations = getOperations(text_file)
            note = "wsad z django"  # temporary
            user_name = "admin"  # temporary
            user = User.objects.get(username=user_name)
            try:
                bank_obj = BankStatement(
                    date=getStatementDate(text_file),
                    user=user,
                    notes=note,
                )
                bank_obj.save()
            except IntegrityError:
                return Response("Confilct", status=409)

            for operation in operations:
                operation_obj = Operations(**operation, user=user, bank_statement=bank_obj)
                operation_obj.save()

        return Response("OK", status=200)

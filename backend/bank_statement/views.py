from django.contrib import messages
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
        if request.method == "POST":
            for name, file in request.FILES.items():
                file_name = default_storage.save("backend/bank_statement/store/" + str(name), file)
                text_file = getTextPdf(file_name)
                operations = getOperations(text_file)
                note = "wsad z django"
                user_name = "admin"
                try:
                    bank_obj = BankStatement(
                        date=getStatementDate(text_file),
                        user=User.objects.get(username=user_name),
                        notes=note,
                    )
                    bank_obj.save()
                except IntegrityError:
                    messages.error(request, "Statement already exists in the database.")
                    return Response()
                else:
                    for operation in operations:
                        operation_obj = Operations(
                            **operation, user=User.objects.get(username=user_name), bank_statement=bank_obj
                        )
                        operation_obj.save()
        else:
            messages.error(request, "Method is not POST type")
        return Response()

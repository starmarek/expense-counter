from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
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

    # TODO: przy wprowadzaniu wyciagow trzeba zapytac usera o potencjalne notatki do wyciagu
    # TODO: zsynchronizowac nazwy pol w operations aby podawac gotowy slownik parametrow
    # TODO: wyslac z frontendu odpowiedniego usera
    # TODO: Dodac wszystkie pola z Operations + zmiana amount na value
    @action(detail=False, methods=["post"])
    def loader(self, request):
        if request.method == "POST":
            for name, file in request.FILES.items():
                text_file = getTextPdf(ContentFile(file.read()))
                operations = getOperations(text_file)
                note = "wsad z django"
                user_name = "userdjango"
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
                    for row in operations:
                        insert_time = row["date"] + " " + row["time"]
                        oper_obj = Operations(
                            datetime=insert_time,
                            user=User.objects.get(username=user_name),
                            category=row["category"],
                            operation_type=row["operation_type"],
                            bank_statement=bank_obj,
                            isExpense=False,
                        )
                        oper_obj.save()
        else:
            messages.error(request, "Method is not POST type")
        return Response()

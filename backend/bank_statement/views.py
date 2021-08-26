from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db.utils import IntegrityError
from pdfminer.pdfparser import PDFSyntaxError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.operations.models import Operations
from backend.settings import STORE_PATH

from .models import BankStatement
from .scraper import getOperations, getStatementDate, getTextPdf
from .serializers import BankStatementSerializer


class BankStatementViewSet(viewsets.ModelViewSet):
    queryset = BankStatement.objects.all()
    serializer_class = BankStatementSerializer

    @action(detail=False, methods=["post"])
    def loader(self, request):
        if len(request.FILES) == 0:
            return Response("Range Not Satisfiable", status=416)

        for name, file in request.FILES.items():
            file_name = default_storage.save(STORE_PATH + name, file)
            note = request.POST["note"]
            user = User.objects.get(username=request.POST["user"])
            try:
                text_file = getTextPdf(file_name)
                operations = getOperations(text_file)
                date1 = getStatementDate(text_file)
                bank_obj = BankStatement(
                    date=date1,
                    user=user,
                    notes=note,
                )
                bank_obj.save()
            except PDFSyntaxError:
                return Response("Unsupported Media Type", status=415)
            except AttributeError:
                return Response("Not Acceptable", status=406)
            except IntegrityError:
                return Response("Conflict", status=409)
            except Exception as e:
                return Response(e, status=400)

            for operation in operations:
                operation_obj = Operations(**operation, user=user, bank_statement=bank_obj)
                operation_obj.save()

        return Response("OK", status=200)

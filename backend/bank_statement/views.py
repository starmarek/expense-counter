import datetime
import os

from django.contrib.auth.models import User
from django.core.files import File
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from pdfminer.pdfparser import PDFSyntaxError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.operations.models import Operations
from backend.settings import DATE_PATTERN, STORE_PATH

from .models import BankStatement
from .scraper import getOperations, getStatementDate, getTextPdf
from .serializers import BankStatementSerializer


class BankStatementFilter(filters.FilterSet):
    user = filters.NumberFilter(field_name="user")

    ordering = filters.OrderingFilter(fields=(("id", "id"),))

    class Meta:
        model = BankStatement
        fields = ["user"]


class BankStatementViewSet(viewsets.ModelViewSet):
    queryset = BankStatement.objects.all().order_by("id")
    serializer_class = BankStatementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BankStatementFilter

    @action(detail=False, methods=["POST"])
    def loader(self, request):
        if len(request.FILES) == 0:
            return Response("No files to upload", status=416)

        for _, file in request.FILES.items():
            note = request.POST["note"]
            user = User.objects.get(username=request.POST["user"])
            try:
                upload_day = datetime.datetime.now().strftime(DATE_PATTERN)
                bank_obj = BankStatement(
                    date_upload=upload_day,
                    user=user,
                    note=note,
                    file=file,
                    name=file.name,
                )
                bank_obj.save()  # saves file in storage
                text_file = getTextPdf(STORE_PATH + request.POST["filename"])
                operations = getOperations(text_file)
                bank_obj.date = getStatementDate(text_file)
                bank_obj.save()  # update record
            except PDFSyntaxError:
                bank_obj.delete()
                return Response("Unsupported Media Type", status=415)
            except AttributeError:
                bank_obj.delete()
                return Response("Not Acceptable", status=406)
            except IntegrityError:
                name = file.name.split(".")[0]
                del_file = [file for file in os.listdir(STORE_PATH) if file.startswith(name + "_")]
                os.remove(STORE_PATH + del_file[0])
                last_record_id = BankStatement.objects.latest("id").id
                BankStatement.objects.filter(id=last_record_id).delete()
                return Response("Record already exists in database", status=409)
            except Exception as e:
                bank_obj.delete()
                return Response(str(e), status=404)

            for operation in operations:
                operation_obj = Operations(
                    **operation,
                    user=user,
                    bank_statement=bank_obj,
                )
                operation_obj.save()

        return Response("OK", status=200)

    @action(detail=False, methods=["GET"])
    def store(self, request):
        bs = BankStatement.objects.get(pk=request.GET["ID"])
        with open(STORE_PATH + bs.name, "rb") as pdf:
            pdfFile = File(pdf)
            response = HttpResponse(pdfFile.read())
            return response

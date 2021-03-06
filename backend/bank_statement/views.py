import datetime
import os

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
from backend.operations.serializers import OperationsSerializer
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
        file = request.FILES["file"]
        note = request.data["note"]
        user = request.data["user"]
        upload_day = datetime.datetime.now().strftime(DATE_PATTERN)
        tmp = "tmp.pdf"

        try:
            if not os.path.exists(STORE_PATH):
                os.makedirs(STORE_PATH)

            with open(STORE_PATH + tmp, "wb+") as f:
                for chunk in file.chunks():
                    f.write(chunk)

            text_file = getTextPdf(STORE_PATH + tmp)
            operations = getOperations(text_file)
            statement_date = getStatementDate(text_file)

            os.remove(STORE_PATH + tmp)

            bank_serializer = BankStatementSerializer(
                data={
                    "date_upload": upload_day,
                    "date": statement_date,
                    "user": user,
                    "note": note,
                    "file": file,
                    "name": file.name,
                }
            )
            bank_serializer.is_valid(raise_exception=True)
            bank_serializer.save()

        except PDFSyntaxError:  # if file is not pdf but has extent .pdf
            return Response("Unsupported Media Type", status=415)
        except AttributeError:  # if file is pdf but is not statement
            return Response("Not Acceptable PDF File", status=400)
        except IntegrityError:  # if record exists in database
            name = file.name.split(".")[0]
            del_file = [file for file in os.listdir(STORE_PATH) if file.startswith(name + "_")]
            if del_file:
                os.remove(STORE_PATH + del_file[0])
            return Response("Record already exists in database", status=409)
        except Exception:
            return Response("Error not yet handled", status=400)

        detail_category = {
            obj.details: obj.category.name for obj in Operations.objects.all() if obj.category is not None
        }
        for operation in operations:
            category = detail_category[operation["details"]] if operation["details"] in detail_category else None
            operation_serializer = OperationsSerializer(
                data={**operation, "user": user, "bank_statement": bank_serializer.instance.pk, "category": category}
            )
            operation_serializer.is_valid(raise_exception=True)
            operation_serializer.save()

        return Response("OK", status=200)

    @action(detail=False, methods=["GET"])
    def store(self, request):
        bs = BankStatement.objects.get(pk=request.GET["ID"])
        with open(STORE_PATH + bs.name, "rb") as pdf:
            pdfFile = File(pdf)
            response = HttpResponse(pdfFile.read())
            return response

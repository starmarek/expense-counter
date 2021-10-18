from datetime import date, timedelta

import factory
from django.core.files.uploadedfile import SimpleUploadedFile

from ...user.tests.factories import UserFactory
from ..models import BankStatement


class BankStatementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BankStatement

    user = factory.SubFactory(UserFactory)
    note = "fake note"
    date = date.today()
    date_upload = date.today() - timedelta(days=1)
    file = SimpleUploadedFile("file.pdf", b"xxx", content_type="file/pdf")
    name = "file.pdf"

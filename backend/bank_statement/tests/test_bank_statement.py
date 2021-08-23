import datetime
from io import BytesIO
from unittest.mock import ANY, mock_open, patch

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.db.utils import IntegrityError
from pdfminer.pdfparser import PDFSyntaxError

from backend.bank_statement.scraper import getOperations, getStatementDate, getTextPdf
from backend.settings import DATE_PATTERN, STORE_PATH


@pytest.mark.parametrize("date", ["Data: 12.12.2020", "Data: 01.01.1910"])
def test_getStatementDate_correct_date_format(date):
    getStatementDate(date)


@pytest.mark.parametrize("date", ["Data: 12-12-2020", "Data: 2020.09.11"])
def test_getStatementDate_check_Value_error(date):
    with pytest.raises(ValueError):
        getStatementDate(date)


@pytest.mark.parametrize("date", ["Random text", ""])
def test_getStatementDate_check_Attribute_error(date):
    with pytest.raises(AttributeError):
        getStatementDate(date)


def test_getStatementDate_return_correct_date_format():
    raw_date = "12.12.2020"
    expected_date = datetime.datetime.strptime(raw_date, "%d.%m.%Y").strftime(DATE_PATTERN)

    returned_date = getStatementDate("Data: " + raw_date)

    assert returned_date == expected_date


@patch("backend.bank_statement.scraper.PDFPage")
@patch("backend.bank_statement.scraper.PDFPageInterpreter")
@patch("backend.bank_statement.scraper.TextConverter")
@patch("backend.bank_statement.scraper.LAParams")
@patch("backend.bank_statement.scraper.StringIO")
@patch("backend.bank_statement.scraper.PDFResourceManager")
def test_getTextPdf_check_if_given_file_is_called_in_open(
    rsr_Mock, ret_Mock, lap_Mock, device_Mock, inter_Mock, page_Mock
):
    pdf_file = "path/to/statement"
    with patch("builtins.open", mock_open(read_data=pdf_file)) as m:
        getTextPdf(pdf_file)
    m.assert_called_with(pdf_file, "rb")


@patch("backend.bank_statement.scraper.PDFPage")
@patch("backend.bank_statement.scraper.PDFPageInterpreter")
@patch("backend.bank_statement.scraper.TextConverter")
@patch("backend.bank_statement.scraper.LAParams")
@patch("backend.bank_statement.scraper.StringIO")
@patch("backend.bank_statement.scraper.PDFResourceManager")
def test_getTextPdf_PDFSyntax_error(rsr_Mock, ret_Mock, lap_Mock, device_Mock, inter_Mock, page_Mock):
    pdf_file = r"file"
    inter_Mock.side_effect = PDFSyntaxError()
    with patch("builtins.open", mock_open(read_data=pdf_file)):
        with pytest.raises(PDFSyntaxError):
            getTextPdf(pdf_file)


@pytest.fixture
def raw_text_pattern():
    return "Saldo\n\n06.05.2021\n\n1626MX20705169010\n\nZAKUP PRZY UŻYCIU KARTY\n\n-49,80\n\n3 210,54\n\n05.05.2021\n\nKarta:516931******7069 Godz.17:24:02 Lokalizacja: Boleslawiec PL Apteka Centrum\nSUPERNOV Nr ref: 75275421121310690607092\nKwota oryg.: 49,80 PLN\n\nSaldo końcowe"


def test_getOperations_text_has_correct_format_to_scrap(raw_text_pattern):
    assert "Saldo" and "Saldo końcowe" in raw_text_pattern


@pytest.mark.parametrize("field", ["date", "time", "details", "value", "operation_type", "balance"])
def tets_getOperations_has_required_field(field, raw_text_pattern):
    result = getOperations(raw_text_pattern)
    assert field in result[0]


def test_getOperations_returned_list_filled_with_dictionaries(raw_text_pattern):
    result = getOperations(raw_text_pattern)
    assert type(result[0]) is dict


@pytest.mark.django_db
@patch("backend.bank_statement.views.default_storage")
@patch("backend.bank_statement.views.getTextPdf")
@patch("backend.bank_statement.views.getOperations")
@patch("backend.bank_statement.views.BankStatement")
@patch("backend.bank_statement.views.User")
@patch("backend.bank_statement.views.getStatementDate")
def test_loader_successful_response(
    date_Mock,
    user_Mock,
    bs_Mock,
    getOper_Mock,
    getText_Mock,
    def_storage_Mock,
    api_client,
):
    tmp_file = SimpleUploadedFile("file.pdf", b"xxx", content_type="file/pdf")
    result = api_client.post("/api/bank_statement/loader/", {"file": tmp_file}, format="multipart")
    assert result.status_code == 200


@pytest.mark.django_db
@patch("backend.bank_statement.views.default_storage")
@patch("backend.bank_statement.views.getTextPdf")
@patch("backend.bank_statement.views.getOperations")
@patch("backend.bank_statement.views.BankStatement")
@patch("backend.bank_statement.views.User")
@patch("backend.bank_statement.views.getStatementDate")
def test_loader_integrity_error_response(
    date_Mock,
    user_Mock,
    bs_Mock,
    getOper_Mock,
    getText_Mock,
    def_storage_Mock,
    api_client,
):
    bs_Mock.side_effect = IntegrityError()
    tmp_file = SimpleUploadedFile("file.pdf", b"xxx", content_type="file/pdf")
    result = api_client.post("/api/bank_statement/loader/", {"file": tmp_file}, format="multipart")
    assert result.status_code == 409


@pytest.mark.django_db
@patch("backend.bank_statement.views.default_storage")
@patch("backend.bank_statement.views.getTextPdf")
@patch("backend.bank_statement.views.getOperations")
@patch("backend.bank_statement.views.BankStatement")
@patch("backend.bank_statement.views.User")
@patch("backend.bank_statement.views.getStatementDate")
def test_loader_no_files_in_request(
    date_Mock,
    user_Mock,
    bs_Mock,
    getOper_Mock,
    getText_Mock,
    def_storage_Mock,
    api_client,
):
    result = api_client.post("/api/bank_statement/loader/", format="multipart")
    assert result.status_code == 406


@pytest.mark.django_db
@patch("backend.bank_statement.views.default_storage")
@patch("backend.bank_statement.views.getTextPdf")
@patch("backend.bank_statement.views.getOperations")
@patch("backend.bank_statement.views.BankStatement")
@patch("backend.bank_statement.views.User")
@patch("backend.bank_statement.views.getStatementDate")
def test_loader_correct_bank_statement_model_calls(
    date_Mock,
    user_Mock,
    bs_Mock,
    getOper_Mock,
    getText_Mock,
    def_storage_Mock,
    api_client,
):
    tmp_file = SimpleUploadedFile("file.pdf", b"xxx", content_type="file/pdf")
    api_client.post("/api/bank_statement/loader/", {"file": tmp_file}, format="multipart")
    bs_Mock.assert_called_with(date=date_Mock(), user=user_Mock.objects.get(), notes="wsad z django")


@pytest.mark.django_db
@patch("backend.bank_statement.views.default_storage")
@patch("backend.bank_statement.views.getTextPdf")
@patch("backend.bank_statement.views.getOperations")
@patch("backend.bank_statement.views.User")
@patch("backend.bank_statement.views.BankStatement")
@patch("backend.bank_statement.views.getStatementDate")
@patch("backend.bank_statement.views.Operations")
def test_loader_correct_operations_model_calls(
    oper_Mock,
    date_Mock,
    bs_Mock,
    user_Mock,
    getOper_Mock,
    getText_Mock,
    def_storage_Mock,
    api_client,
):
    tmp_file = SimpleUploadedFile("file.pdf", b"xxx", content_type="file/pdf")
    getOper_Mock.return_value = [
        {
            "date": "2021-01-01",
            "details": "empty",
            "value": "12.00",
            "balance": "100.00",
            "operation_type": "card",
            "time": "00:00",
        }
    ]

    api_client.post("/api/bank_statement/loader/", {"file": tmp_file}, format="multipart")
    oper_Mock.assert_called_with(
        **getOper_Mock.return_value[0],
        user=user_Mock.objects.get(),
        bank_statement=bs_Mock(),
    )


@pytest.mark.django_db
@patch("backend.bank_statement.views.default_storage")
@patch("backend.bank_statement.views.getTextPdf")
@patch("backend.bank_statement.views.getOperations")
@patch("backend.bank_statement.views.BankStatement")
@patch("backend.bank_statement.views.User")
@patch("backend.bank_statement.views.getStatementDate")
def test_loader_correct_path_to_save_statements(
    date_Mock,
    user_Mock,
    bs_Mock,
    getOper_Mock,
    getText_Mock,
    def_storage_Mock,
    api_client,
):
    tmp_file = InMemoryUploadedFile(BytesIO(), "file", "file.pdf", None, len(BytesIO().getvalue()), None)
    api_client.post("/api/bank_statement/loader/", {"file": tmp_file})
    def_storage_Mock.save.assert_called_with(STORE_PATH + tmp_file.field_name, ANY)

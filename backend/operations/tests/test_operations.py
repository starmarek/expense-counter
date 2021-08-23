from datetime import datetime

import pytest

from ...bank_statement.models import BankStatement
from ...operations.models import Operations
from ...operations.tests.factories import OperationFactory
from ...operations.views import OperationsFilter


@pytest.mark.django_db
def test_operation_viewset_return_paginated_response_if_page_param_in_req(api_client, operation):
    resp = api_client.get("/api/operations/?page=1")

    assert resp.status_code == 200
    assert "results" in resp.data


@pytest.mark.django_db
def test_operation_viewset_dont_return_paginated_response_if_page_param_not_in_req(api_client, operation):
    resp = api_client.get("/api/operations/")

    assert resp.status_code == 200
    assert "results" not in resp.data


@pytest.mark.django_db
@pytest.mark.parametrize("order", ["-" + x for x in OperationsFilter.get_filters()["ordering"].param_map.values()])
def test_operation_viewset_return_ordered_response_if_order_desc(api_client, operation, order, operation_factory):
    operation_factory(
        bank_statement=BankStatement.objects.get(id=1),
        date="2021-07-18",
        time="00:00:00",
        value="72.00",
        balance="2400.00",
        operation_type="inny_typ",
    )
    resp = api_client.get("/api/operations/?page=1&ordering=" + order)

    assert resp.status_code == 200
    assert resp.data["results"] == sorted(resp.data["results"], key=lambda k: k[order[1:]], reverse=True)


@pytest.mark.django_db
@pytest.mark.parametrize("order", [x for x in OperationsFilter.get_filters()["ordering"].param_map.values()])
def test_operation_viewset_return_ordered_response_if_order_asc(api_client, operation, order, operation_factory):
    operation_factory(
        bank_statement=BankStatement.objects.get(id=1),
        date="2021-07-18",
        time="00:00:00",
        value="72.00",
        balance="2400.00",
        operation_type="inny_typ",
    )
    resp = api_client.get("/api/operations/?page=1&ordering=" + order)

    assert resp.status_code == 200
    assert resp.data["results"] == sorted(resp.data["results"], key=lambda k: k[order], reverse=False)


@pytest.mark.django_db
def test_operation_viewset_return_ordered_response_if_the_same_elements_in_db(
    api_client, operation, operation_factory
):
    OperationFactory.create_batch(10, bank_statement=BankStatement.objects.get(id=1))
    resp = api_client.get("/api/operations/?page=1&ordering=-date")

    assert resp.status_code == 200
    assert resp.data["results"] == sorted(resp.data["results"], key=lambda k: k["date"], reverse=True)


@pytest.mark.django_db
def test_operation_viewset_return_filtered_by_date_response_if_filter_in_req_and_in_db(api_client, operation):
    resp = api_client.get("/api/operations/?page=1&date=" + str(datetime.now().date()))

    assert resp.status_code == 200
    assert resp.data["results"][0].get("date") == str(datetime.now().date())


@pytest.mark.django_db
def test_operation_viewset_return_filtered_by_date_response_if_filter_in_req_but_not_in_db(api_client, operation):
    resp = api_client.get("/api/operations/?page=1&date=2020-09-16")

    assert resp.status_code == 200
    assert len(resp.data["results"]) == 0


@pytest.mark.django_db
def test_operation_viewset_return_filtered_by_value_response_if_filtermin_and_filtermax_in_req_and_in_db(
    api_client, operation
):
    resp = api_client.get("/api/operations/?page=1&value_min=0&value_max=100")

    assert resp.status_code == 200
    assert resp.data["results"][0].get("value") == "69.00"


@pytest.mark.django_db
def test_operation_viewset_return_filtered_by_value_response_if_filtermin_and_filtermax_in_req_but_not_in_db(
    api_client, operation
):
    resp = api_client.get("/api/operations/?page=1&value_min=0&value_max=10")

    assert resp.status_code == 200
    assert len(resp.data["results"]) == 0


@pytest.mark.django_db
def test_operation_viewset_return_filtered_by_value_response_if_filtermin_in_req_and_in_db(api_client, operation):
    resp = api_client.get("/api/operations/?page=1&value_min=0")

    assert resp.status_code == 200
    assert resp.data["results"][0].get("value") == "69.00"


@pytest.mark.django_db
def test_operation_viewset_return_filtered_by_value_response_if_filtermax_in_req_and_in_db(api_client, operation):
    resp = api_client.get("/api/operations/?page=1&value_max=100")

    assert resp.status_code == 200
    assert resp.data["results"][0].get("value") == "69.00"


@pytest.mark.django_db
def test_operation_viewset_return_filtered_by_category_response_if_filter_in_req_and_in_db(api_client, operation):
    resp = api_client.get("/api/operations/?page=1&category=")

    assert resp.status_code == 200
    assert resp.data["results"][0].get("category") == ""


@pytest.mark.django_db
def test_operation_viewset_return_filtered_by_category_response_if_filter_in_req_but_not_in_db(api_client, operation):
    resp = api_client.get("/api/operations/?page=1&category=Housing")

    assert resp.status_code == 200
    assert len(resp.data["results"]) == 0


@pytest.mark.django_db
@pytest.mark.parametrize("choice", [x[0] for x in Operations.CHOICES])
def test_operation_viewset_return_filtered_by_operationtype_response_if_filter_in_req_and_in_db(
    api_client, operation, choice, operation_factory
):
    operation_factory(bank_statement=BankStatement.objects.get(id=1), operation_type=choice)
    resp = api_client.get("/api/operations/?page=1&operation_type=" + choice)

    assert resp.status_code == 200
    assert resp.data["results"][0].get("operation_type") == choice


@pytest.mark.django_db
@pytest.mark.parametrize("choice", [x[0] for x in Operations.CHOICES])
def test_operation_viewset_return_filtered_by_operationtype_response_if_filter_in_req_but_not_in_db(
    api_client, operation, choice
):
    resp = api_client.get("/api/operations/?page=1&operation_type=" + choice)

    assert resp.status_code == 200
    assert len(resp.data["results"]) == 0

import pytest


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
